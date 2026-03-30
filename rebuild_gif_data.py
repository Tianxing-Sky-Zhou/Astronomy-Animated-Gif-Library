#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(".").resolve()
MASTER_CSV = REPO_ROOT / "Astronomy Animated Gif Library Catalog.csv"
REPO_CSV = REPO_ROOT / "gif_data.csv"

def load_catalog(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Cannot find catalog file: {path}")
    df = pd.read_csv(path)
    df.columns = [str(c).strip() for c in df.columns]
    return df

def normalize_flag(value) -> str:
    if pd.isna(value):
        return "n"
    s = str(value).strip().lower()
    if s in {"y", "yes", "true", "1"}:
        return "y"
    return "n"

def find_column(df: pd.DataFrame, choices: list[str], required: bool = True) -> str | None:
    lower_cols = {c.lower(): c for c in df.columns}
    for choice in choices:
        if choice.lower() in lower_cols:
            return lower_cols[choice.lower()]
    if required:
        raise ValueError(f"Could not find any of these columns: {choices}\nFound columns: {list(df.columns)}")
    return None

def find_tag_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c.strip().lower().startswith("tag")]

def strip_gif_suffix(s: str) -> str:
    s = str(s).strip()
    if s.lower().endswith(".gif"):
        s = s[:-4]
    return s

def build_rows(df: pd.DataFrame) -> list[list[str]]:
    col_name = find_column(df, ["name"])
    col_display = find_column(df, ["display_name", "display name"])
    col_chapter = find_column(df, ["chapter(int)", "chapter", "chapter int"])
    col_source = find_column(df, ["source code (y/n)", "source code"])
    col_gifimg = find_column(df, ["gif images (y/n)", "gif images"])
    col_supp = find_column(
        df,
        ["supplemental material (y/n)", "supplemental materials (y/n)", "supplmental materials (y/n)"]
    )
    tag_cols = find_tag_columns(df)

    rows = []
    for _, row in df.iterrows():
        if pd.isna(row[col_display]) or pd.isna(row[col_chapter]):
            continue

        name = strip_gif_suffix(row[col_name])
        display_name = str(row[col_display]).strip()

        try:
            chapter = str(int(float(row[col_chapter])))
        except Exception:
            continue

        source_code = normalize_flag(row[col_source])
        gif_images = normalize_flag(row[col_gifimg])
        supplemental = normalize_flag(row[col_supp])

        tags = []
        for tc in tag_cols:
            val = row[tc]
            if pd.notna(val):
                sval = str(val).strip()
                if sval:
                    tags.append(sval)

        rows.append([
            name,
            display_name,
            "",   # file_name to be filled later
            chapter,
            source_code,
            gif_images,
            supplemental,
            *tags,
        ])
    return rows

def write_repo_csv(path: Path, rows: list[list[str]]) -> None:
    base_header = [
        "name",
        "display_name",
        "file_name",
        "chapter(int)",
        "source code (y/n)",
        "gif images (y/n)",
        "supplemental material (y/n)",
    ]
    max_tags = 0
    for row in rows:
        max_tags = max(max_tags, max(0, len(row) - 7))

    header = base_header + [f"Tag {i}" for i in range(1, max_tags + 1)]
    target_len = len(header)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            padded = row + [""] * (target_len - len(row))
            writer.writerow(padded[:target_len])

def main():
    df = load_catalog(MASTER_CSV)
    rows = build_rows(df)
    write_repo_csv(REPO_CSV, rows)
    print(f"Wrote {len(rows)} rows to {REPO_CSV}")

if __name__ == "__main__":
    main()