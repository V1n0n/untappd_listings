#!/usr/bin/env python3

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Optional


def normalize(text: object) -> str:
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip().lower()


def parse_number(raw: str) -> Optional[int]:
    """Parse '1,234', '1.234', '12k', '12,3k' etc. to int."""
    if not raw:
        return None
    value = raw.strip().lower().replace("ratings", "").replace("rating", "").strip()
    multiplier = 1
    if value.endswith("k"):
        multiplier = 1000
        value = value[:-1]
    if value.endswith("m"):
        multiplier = 1_000_000
        value = value[:-1]

    value = value.replace(" ", "")
    if multiplier == 1:
        # removal of any str notation of thousands.
        value = value.replace(",", "").replace(".", "")
        try:
            return int(value)
        except ValueError:
            return None

    # k/m notation can contain decimal.
    value = value.replace(",", ".")
    try:
        return int(float(value) * multiplier)
    except ValueError:
        return None

def detect_csv_delimiter(path: Path) -> str:
    sample = path.read_text(encoding="utf-8-sig", errors="replace")[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        return dialect.delimiter
    except csv.Error:
        return ","