#!/usr/bin/env python3
"""
Batch translator script that:  
1. Splits words into chunks respecting 5000 character limit per request
2. Translates multiple words per request to reduce API calls
3. Saves results incrementally to JSON
4. Resumes from previous progress
"""

import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from deep_translator import GoogleTranslator
from threading import Lock
from tqdm import tqdm

INPUT_FILE = 'en.txt'
OUTPUT_FILE = 'en.json'
MAX_WORKERS = 12
MAX_CHARS = 5000  # Maximum characters per request (API limit)
SAVE_EVERY = 1  # Save after each batch

lock = Lock()


def load_words(input_file):
    """Load words from file, handling multiple words per line."""
    words = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line. strip()
            if line: 
                words.append(line)
    return words


def chunk_words_by_chars(words, max_chars):
    """
    Split words into chunks respecting character limit.
    Each chunk is joined by newlines.
    """
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        # Calculate length with newline delimiter
        word_length = len(word) + 1  # +1 for newline
        
        # If adding this word exceeds limit, start new chunk
        if current_length + word_length > max_chars and current_chunk:
            chunks. append(current_chunk)
            current_chunk = []
            current_length = 0
        
        # Add word to current chunk
        current_chunk.append(word)
        current_length += word_length
    
    # Add remaining words
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks


def translate_batch(word_list, batch_num):
    """Translate a batch of words by joining them and splitting result."""
    if not word_list:
        return {}
    
    # Join words with newlines for batch translation
    batch_text = '\n'.join(word_list)
    batch_size = len(word_list)
    batch_chars = len(batch_text)
    
    for attempt in range(3):
        try:
            translator = GoogleTranslator(source='en', target='fa')
            translated_text = translator.translate(batch_text)
            
            # Split the translated text back into individual words
            translated_words = translated_text.split('\n')
            
            # Create mapping
            result = {}
            for i, original in enumerate(word_list):
                if i < len(translated_words):
                    translated = translated_words[i]. strip()
                    if translated: 
                        result[original] = translated
                else:
                    print(f"[WARN] Batch {batch_num}: No translation for '{original}'")
            
            print(f"[OK] Batch {batch_num}: Translated {len(result)}/{batch_size} words ({batch_chars} chars)")
            return result
            
        except Exception as e:
            print(f"[WARN] Batch {batch_num} failed (attempt {attempt + 1}/3): {e}")
            time.sleep(1 + attempt)  # Exponential backoff
    
    print(f"[ERROR] Batch {batch_num}:  Failed after 3 attempts, skipping {batch_size} words")
    return {}


def load_existing_results(output_file):
    """Load previously translated results."""
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except Exception as e:
            print(f'[WARN] Could not load existing {output_file}: {e}')
    return {}


def save_results_atomic(results, output_file):
    """Save results to disk atomically."""
    tmp = output_file + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    os.replace(tmp, output_file)


def main():
    print('[INFO] Loading words from file...')
    words = load_words(INPUT_FILE)
    print(f'[INFO] Loaded {len(words)} words total')

    # Load any previously translated results
    results = load_existing_results(OUTPUT_FILE)
    print(f'[INFO] Loaded {len(results)} existing translations from {OUTPUT_FILE}')

    # Determine which words still need translation
    to_translate = [w for w in words if w not in results]
    total_remaining = len(to_translate)
    print(f'[INFO] {total_remaining} words to translate')

    if total_remaining == 0:
        print('[INFO] Nothing to do.  Exiting.')
        return

    # Create chunks respecting 5000 character limit
    chunks = chunk_words_by_chars(to_translate, MAX_CHARS)
    total_chunks = len(chunks)
    
    # Calculate stats
    chunk_sizes = [len(c) for c in chunks]
    chunk_chars = [len('\n'.join(c)) for c in chunks]
    
    print(f'[INFO] Split into {total_chunks} chunks (max {MAX_CHARS} characters per batch)')
    print(f'[INFO] Chunk word counts: min={min(chunk_sizes)}, max={max(chunk_sizes)}, avg={sum(chunk_sizes)//len(chunk_sizes)}')
    print(f'[INFO] Chunk char counts: min={min(chunk_chars)}, max={max(chunk_chars)}, avg={sum(chunk_chars)//len(chunk_chars)}')
    print()

    new_count = 0
    pbar = tqdm(total=total_remaining, desc='Translating', unit='word')

    try:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Submit all chunks
            future_map = {
                executor.submit(translate_batch, chunk, i): i 
                for i, chunk in enumerate(chunks)
            }

            for future in as_completed(future_map):
                chunk_idx = future_map[future]
                try:
                    batch_results = future.result()
                    
                    with lock:
                        # Add results to dictionary
                        for word, translation in batch_results.items():
                            if translation and translation. strip():
                                results[word] = translation
                                new_count += 1
                        
                        # Update progress bar
                        pbar.update(len(batch_results))
                        
                        # Save after each batch
                        if SAVE_EVERY > 0:
                            print(f'[INFO] Batch {chunk_idx + 1}/{total_chunks} completed. '
                                  f'Total new translations: {new_count}')
                            save_results_atomic(results, OUTPUT_FILE)

                except Exception as e:
                    print(f"[ERROR] Unexpected error processing chunk {chunk_idx}: {e}")
                    pbar.update(len(chunks[chunk_idx]))

    except KeyboardInterrupt:
        print('\n[INFO] Interrupted by user.  Saving progress...')
    finally:
        # Ensure final save
        with lock:
            save_results_atomic(results, OUTPUT_FILE)
        pbar.close()
        print(f'\n[SAVED] Final results saved to {OUTPUT_FILE}')
        print(f'[INFO] Total translations in file: {len(results)}')
        print(f'[INFO] New translations in this run: {new_count}')


if __name__ == '__main__':
    main()
