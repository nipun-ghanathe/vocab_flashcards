import csv
from pathlib import Path

import pandas as pd  # type: ignore[import-untyped]
import requests


def verify_dir_exists_else_create(dir_path: Path) -> bool:
    """
    Checks whether or not the given directory exists, if not then creates it.

    Returns
    -------
        True if the path exists and is a directory
        False if either the path doesn't exist or isn't a directory

    """
    dir_exists = dir_path.exists() and dir_path.is_dir()
    if not dir_exists:
        dir_path.mkdir()
    return dir_exists

def download_word_list(url: str, out_path: Path) -> None:
    """Download our word list from Cambridge Online Dictionary."""
    # Spoof browser headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("Request Timed out!")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    out_path.write_bytes(response.content)

    print(f"Downloaded word list from Cambridge Online Dictionary to {out_path}")


def read_sorted_csv_rows(path: Path, skip_lines: int = 2) -> list[list[str]]:
    """Read and sort CSV rows, skipping the specified number of initial lines and return a list."""
    with path.open(newline="", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = sorted(csv_reader)[skip_lines:]
    return rows


def write_tsv(path: Path, rows: list[list[str]]) -> None:
    """Write a list of rows to a tsv file."""
    with path.open("w", newline="", encoding="utf-8") as file:
        csv_writer = csv.writer(file, delimiter="\t", lineterminator="\n")
        csv_writer.writerows(rows)


def format_word(part: str, word: str) -> str:
    """Return formatted key for the flashcard."""
    return f"({part}) {word}"


def get_word_meaning_list(rows: list[list[str]]) -> list[list[str]]:
    """Get a grouped 'word -> meaning' list."""
    # rows.sort()  # Rows must be sorted for grouping
    grouped_rows: list[list[str]] = []
    prev_key = ""
    for word, part, meaning in rows:
        key = format_word(part, word)
        if key != prev_key:
            grouped_rows.append([key, meaning])
        elif grouped_rows[-1][1].startswith("-"):
            grouped_rows[-1][1] += f"\n- {meaning}"
        else:
            grouped_rows[-1][1] = f"- {grouped_rows[-1][1]}\n- {meaning}"
        prev_key = key
    return grouped_rows


def main():
    # Paths and URLs
    url = "https://dictionary.cambridge.org/us/plus/wordlist/146100558/export"
    excel_path = Path("data/nipun-word-list.xlsx")
    csv_path = Path("data/nipun-word-list.csv")
    word_meaning_path = Path("data/word-meaning.tsv")
    meaning_word_path = Path("data/meaning-word.tsv")

    # Ensure that the directory exists else create it
    verify_dir_exists_else_create(excel_path.parent)

    # Download the word list from Cambridge Online Dictionary
    download_word_list(url, excel_path)

    # Convert excel to csv
    pd.read_excel(excel_path).to_csv(csv_path, index=False)

    # Read the CSV
    csv_rows = read_sorted_csv_rows(csv_path)

    # Write word -> meaning (grouped)
    word_meaning = get_word_meaning_list(csv_rows)
    write_tsv(word_meaning_path, word_meaning)

    # Write meaning -> word (ungrouped)
    meaning_word = [
        [format_word(part, meaning), word] for word, part, meaning in csv_rows
    ]
    write_tsv(meaning_word_path, meaning_word)


if __name__ == "__main__":
    main()
