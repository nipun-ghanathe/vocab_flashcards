import csv
from pathlib import Path

import pandas as pd  # type: ignore[import-untyped]

# Paths
excel_path = Path("data/nipun-word-list.xlsx")
csv_path = Path("data/nipun-word-list.csv")
word_meaning_path = Path("data/word-meaning.csv")
meaning_word_path = Path("data/meaning-word.csv")

# Convert excel to csv
pd.read_excel(excel_path).to_csv(csv_path, index=False)

with csv_path.open(newline="", encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip header
    next(csv_reader)  # Skip metadata

    # Load data into memory (since generators can be used only once)
    rows = list(csv_reader)

# Preprocess data (wrap part of speech in parentheses)
for row in rows:
    row[1] = f"({row[1]})"

# Write word -> meaning
with word_meaning_path.open("w", newline="", encoding="utf-8") as file:
    csv_writer = csv.writer(file, delimiter="\t", lineterminator="\n")
    for word, part, definition in rows:
        csv_writer.writerow([f"{part} {word}", definition])

# Write meaning -> word
with meaning_word_path.open("w", newline="", encoding="utf-8") as file:
    csv_writer = csv.writer(file, delimiter="\t", lineterminator="\n")
    for word, part, definition in rows:
        csv_writer.writerow([f"{part} {definition}", word])
