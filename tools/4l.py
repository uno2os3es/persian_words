from pathlib import Path

json_file = Path("dic2.json")
out_file = Path("words.txt")

good_lines = []
bad_lines = []

with json_file.open("r", encoding="utf-8") as f:
    for line in f:
        if line.count('"') > 4:
            bad_lines.append(line)
        else:
            good_lines.append(line)

# overwrite dic.json with clean lines
json_file.write_text("".join(good_lines), encoding="utf-8")

# save removed lines
out_file.write_text("".join(bad_lines), encoding="utf-8")

print(f"Removed {len(bad_lines)} lines → {out_file}")
print(f"Updated {json_file} in place")