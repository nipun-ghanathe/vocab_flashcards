import csv
from pathlib import Path

import pandas as pd  # type: ignore[import-untyped]


def read_sorted_csv_rows(path: Path, skip_lines: int = 2) -> list[list[str]]:
    """Read rows from a csv file ignoring specified number of initial rows."""
    with path.open(newline="", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = sorted(csv_reader)[skip_lines:]
    return rows


def write_tsv(path: Path, rows: list[list[str]]) -> None:
    """Write a list of rows to a tsv (tab-separated csv) file."""
    with path.open("w", newline="", encoding="utf-8") as file:
        csv_writer = csv.writer(file, delimiter="\t", lineterminator="\n")
        csv_writer.writerows(rows)


def get_word_meaning_list(rows: list[list[str]]) -> list[list[str]]:
    """Get a gropued word -> meaning list."""
    rows.sort()  # Ensure sorted for grouping
    grouped = []
    prev_word = ""
    for word, part, definition in rows:
        key = f"({part}) {word}"
        if key != prev_word:
            grouped.append([word, definition])
        else:
            grouped[-1][1] = f"- {grouped[-1][1]}\n- {definition}"
        prev_word = key
    return grouped


def main():
    # Paths
    excel_path = Path("data/nipun-word-list.xlsx")
    csv_path = Path("data/nipun-word-list.csv")
    word_meaning_path = Path("data/word-meaning.csv")
    meaning_word_path = Path("data/meaning-word.csv")

    # Convert excel to csv
    pd.read_excel(excel_path).to_csv(csv_path, index=False)

    rows = read_sorted_csv_rows(csv_path)

    # Write word -> meaning (grouped)
    word_meaning = get_word_meaning_list(rows)
    write_tsv(word_meaning_path, word_meaning)

    # Write meaning -> word (ungrouped)
    meaning_word = [[f"({part}) {definition}", word] for word, part, definition in rows]
    write_tsv(meaning_word_path, meaning_word)


if __name__ == "__main__":
    main()
