import re
import os
import pickle
from collections import Counter


class SpellCorrector:
    NWORDS = None

    @staticmethod
    def words(text: str):
        # Extract Persian words
        return re.findall(r'[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]+', text.lower())

    @staticmethod
    def train(features):
        return Counter(features)

    @staticmethod
    def edits1(word: str):
        alphabet = [
            'ٍ',
            'َ',
            'ُ',
            'ِ',
            'ء',
            'ئ',
            'ی',
            'ه',
            'و',
            'ن',
            'م',
            'ل',
            'گ',
            'ک',
            'ق',
            'ف',
            'غ',
            'ع',
            'ظ',
            'ط',
            'ض',
            'ص',
            'ش',
            'س',
            'ژ',
            'ز',
            'ر',
            'ذ',
            'د',
            'خ',
            'ح',
            'چ',
            'ج',
            'ث',
            'ت',
            'پ',
            'ب',
            'آ',
            'ا',
            'ً',
            'ٌ',
        ]
        n = len(word)
        edits = []

        # Deletion and substitution
        for i in range(n):
            edits.append(word[:i] + word[i + 1:])
            for c in alphabet:
                edits.append(word[:i] + c + word[i + 1:])

        # Transposition
        for i in range(n - 1):
            edits.append(word[:i] + word[i + 1] + word[i] + word[i + 2:])

        # Insertion
        for i in range(n + 1):
            for c in alphabet:
                edits.append(word[:i] + c + word[i:])

        return edits

    @classmethod
    def known_edits2(cls, word):
        known = []
        for e1 in cls.edits1(word):
            for e2 in cls.edits1(e1):
                if e2 in cls.NWORDS:
                    known.append(e2)
        return known

    @classmethod
    def known(cls, words):
        return [w for w in words if w in cls.NWORDS]

    @classmethod
    def correct(cls, word: str):
        word = word.strip()
        if not word:
            return word
        if word.isnumeric():
            return word

        word = word.lower()

        if cls.NWORDS is None:
            if not os.path.exists('serialized_dictionary.pkl'):
                with open('big.txt', encoding='utf-8') as f:
                    cls.NWORDS = cls.train(cls.words(f.read()))
                with open('serialized_dictionary.pkl', 'wb') as fp:
                    pickle.dump(cls.NWORDS, fp)
            else:
                with open('serialized_dictionary.pkl', 'rb') as fp:
                    cls.NWORDS = pickle.load(fp)

        candidates = []
        if cls.known([word]):
            return word
        elif tmp_candidates := cls.known(cls.edits1(word)):
            candidates.extend(tmp_candidates)
        elif tmp_candidates := cls.known_edits2(word):
            candidates.extend(tmp_candidates)
        else:
            return word

        # Return candidate with highest frequency
        return max(candidates, key=lambda c: cls.NWORDS[c], default=word)


# Example usage:
if __name__ == '__main__':
    print(SpellCorrector.correct(
        'پیرامون'))  # Should return the same if it's in dictionary
