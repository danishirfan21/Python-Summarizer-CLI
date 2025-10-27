from __future__ import annotations
import csv
import json
import os
from typing import List, Dict, Any

def read_text(path: str) -> str:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Input file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def stem_name(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]

def write_json(path: str, data: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def write_csv(path: str, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        # Create an empty CSV with a header to be safe
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["insight"])
        return

    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
