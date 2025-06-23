import csv
from collections import Counter
from pathlib import Path

import pandas as pd  # type: ignore[import-untyped]


def main():
    # Paths
    excel_path = Path("data/nipun-word-list.xlsx")
    csv_path = Path("data/nipun-word-list.csv")
    word_meaning_path = Path("data/word-meaning.csv")
    meaning_word_path = Path("data/meaning-word.csv")

    # Convert excel to csv
    pd.read_excel(excel_path).to_csv(csv_path, index=False)

    with csv_path.open(newline="", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = list(csv_reader)[2:]  # Load data into memory

    # Preprocess data (wrap part of speech in parentheses)
    for row in rows:
        row[1] = f"({row[1]})"

    # Write word -> meaning
    # word_meaning_list = get_word_meaning_list(rows)
    with word_meaning_path.open("w", newline="", encoding="utf-8") as file:
        csv_writer = csv.writer(file, delimiter="\t", lineterminator="\n")
        # csv_writer.writerows(word_meaning_list)
        for word, part, definition in rows:
            csv_writer.writerow([f"{part} {word}", definition])

    # Write meaning -> word
    with meaning_word_path.open("w", newline="", encoding="utf-8") as file:
        csv_writer = csv.writer(file, delimiter="\t", lineterminator="\n")
        for word, part, definition in rows:
            csv_writer.writerow([f"{part} {definition}", word])


# def get_word_meaning_list(rows: list[list]):
#     new_rows = []
#     for word, part, definition in rows:
#         new_rows.append([f"{part} {word}", definition])


if __name__ == "__main__":
    main()
