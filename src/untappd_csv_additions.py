#!/usr/bin/env python3
"""
Adds a CSV with Brewery and beers with Untappd ratings

Install:
  pip install pandas requests beautifulsoup4 rapidfuzz playwright
  playwright install chromium

Usage
  python untappd_csv_additions.py "van moll fest 2026.csv" -o "van moll fest 2026 aangevuld.csv"
  python untappd_csv_additions.py "van moll fest 2026.csv" -o "van moll fest 2026 aangevuld.csv" --limit 10

Optional:
  python untappd_csv_additions.py input.csv -o output.csv --delay 2 --limit 20

Remember:
- Untappd can block traffic and fail.
- Beers that are not found or where the probability is low will be filled in as NA.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Optional

import pandas as pd
import requests

import general_functions
import untappd_functions

RATING_COL = "Untappd Rating"
COUNT_COL = "Ratings count"
BREWERY_COL = "Brouwer"
BEER_COL = "Naam"

def enrich_csv(input_path: Path, output_path: Path, delay: float, limit: Optional[int]) -> None:
    delimiter = general_functions.detect_csv_delimiter(input_path)
    destination_file = pd.read_csv(input_path, sep=delimiter, dtype=str, encoding="utf-8-sig")

    destination_file = destination_file.loc[:, ~destination_file.columns.str.match(r"^Unnamed")]

    required = [BREWERY_COL, BEER_COL]
    missing = [c for c in required if c not in destination_file.columns]
    if missing:
        raise ValueError(f"Ontbrekende verplichte kolommen: {', '.join(missing)}")

    if RATING_COL not in destination_file.columns:
        destination_file[RATING_COL] = ""
    if COUNT_COL not in destination_file.columns:
        destination_file[COUNT_COL] = ""

    session = requests.Session()
    total = len(destination_file) if limit is None else min(limit, len(destination_file))

    for idx, row in destination_file.head(total).iterrows():
        brewery = str(row.get(BREWERY_COL, "")).strip().lower()
        beer = str(row.get(BEER_COL, "")).strip().lower()

        if not brewery or not beer:
            destination_file.at[idx, RATING_COL] = "NA"
            destination_file.at[idx, COUNT_COL] = "NA"
            continue

        print(f"[{idx + 1}/{total}] Zoeken: {brewery} - {beer}", flush=True)
        try:
            result = untappd_functions.lookup_untappd(session, brewery, beer)
        except Exception as exc:
            print(f"  fout: {exc}", file=sys.stderr)
            result = None

        if result is None:
            destination_file.at[idx, RATING_COL] = "NA"
            destination_file.at[idx, COUNT_COL] = "NA"
            print("  => NA")
        else:
            destination_file.at[idx, RATING_COL] = result.rating
            destination_file.at[idx, COUNT_COL] = result.rating_count
            print(f"  => {result.rating} / {result.rating_count} ratings | match {result.confidence}%")

        time.sleep(delay)

    destination_file.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\nKlaar: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Vul bier-CSV aan met Untappd ratings.")
    parser.add_argument("input", type=Path, help="Pad naar input CSV")
    parser.add_argument("-o", "--output", type=Path, default=Path("untappd_aangevuld.csv"), help="Pad naar output CSV")
    parser.add_argument("--delay", type=float, default=1.5, help="Wachttijd tussen requests in seconden")
    parser.add_argument("--limit", type=int, default=None, help="Alleen eerste N regels verwerken, handig om te testen")
    args = parser.parse_args()

    enrich_csv(args.input, args.output, args.delay, args.limit)


if __name__ == "__main__":
    main()
