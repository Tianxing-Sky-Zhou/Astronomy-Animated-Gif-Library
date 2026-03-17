#!/usr/bin/env python3
from __future__ import annotations

import csv
import subprocess
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(".").resolve()

MASTER_CSV = REPO_ROOT / "Astronomy Animated Gif Library Catalog.csv"
REPO_CSV = REPO_ROOT / "gif_data.csv"
UPDATE_SCRIPT = REPO_ROOT / "update_HTML_files.py"


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


def normalize_slug(value: str) -> str:
    s = str(value).strip()
    if s.lower().endswith(".gif"):
        s = s[:-4]
    s = s.replace(" ", "_")
    return s


def find_column(df: pd.DataFrame, choices: list[str], required: bool = True) -> str | None:
    lower_cols = {c.lower(): c for c in df.columns}
    for choice in choices:
        if choice.lower() in lower_cols:
            return lower_cols[choice.lower()]
    if required:
        raise ValueError(f"Could not find any of these columns: {choices}\nFound columns: {list(df.columns)}")
    return None


def find_tag_columns(df: pd.DataFrame) -> list[str]:
    tag_cols = []
    for c in df.columns:
        cl = c.strip().lower()
        if cl.startswith("tag"):
            tag_cols.append(c)
    return tag_cols


def map_catalog_to_repo_rows(df: pd.DataFrame) -> list[list[str]]:
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
        if pd.isna(row[col_name]) or pd.isna(row[col_display]) or pd.isna(row[col_chapter]):
            continue

        name_slug = normalize_slug(row[col_name])
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

        repo_row = [
            name_slug,
            display_name,
            chapter,
            source_code,
            gif_images,
            supplemental,
            *tags,
        ]
        rows.append(repo_row)

    return rows


def read_existing_repo_csv(path: Path) -> list[list[str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.reader(f))


def merge_rows(existing: list[list[str]], new_rows: list[list[str]]) -> list[list[str]]:
    """
    Merge rows using the first column ('name') as the unique key.
    New catalog rows overwrite matching old rows.
    """
    merged = {}

    if existing:
        first = [x.strip().lower() for x in existing[0]]
        if len(first) >= 1 and first[0] == "name":
            existing_data = existing[1:]
        else:
            existing_data = existing
    else:
        existing_data = []

    for row in existing_data:
        if row:
            merged[row[0]] = row

    for row in new_rows:
        merged[row[0]] = row

    merged_rows = list(merged.values())

    def sort_key(r):
        try:
            ch = int(float(r[2]))
        except Exception:
            ch = 999
        name = r[1].lower() if len(r) > 1 else ""
        return (ch, name)

    return sorted(merged_rows, key=sort_key)


def write_repo_csv(path: Path, rows: list[list[str]]) -> None:
    """
    Write a rectangular CSV with explicit Tag 1, Tag 2, ... columns.
    This is required because pandas.read_csv() expects a consistent number of columns.
    """
    base_header = [
        "name",
        "display_name",
        "chapter(int)",
        "source code (y/n)",
        "gif images (y/n)",
        "supplemental material (y/n)",
    ]

    max_tags = 0
    for row in rows:
        n_tags = max(0, len(row) - 6)
        if n_tags > max_tags:
            max_tags = n_tags

    header = base_header + [f"Tag {i}" for i in range(1, max_tags + 1)]

    padded_rows = []
    target_len = len(header)
    for row in rows:
        padded = row + [""] * (target_len - len(row))
        padded_rows.append(padded[:target_len])

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(padded_rows)


def run_update_script() -> None:
    if not UPDATE_SCRIPT.exists():
        raise FileNotFoundError(f"Cannot find update script: {UPDATE_SCRIPT}")
    subprocess.run(["python", str(UPDATE_SCRIPT)], check=True, cwd=REPO_ROOT)


def main():
    print(f"Reading master catalog from: {MASTER_CSV}")
    df = load_catalog(MASTER_CSV)
    print(f"Loaded {len(df)} rows from master catalog")

    new_rows = map_catalog_to_repo_rows(df)
    print(f"Prepared {len(new_rows)} rows for gif_data.csv")

    existing = read_existing_repo_csv(REPO_CSV)
    merged_rows = merge_rows(existing, new_rows)
    write_repo_csv(REPO_CSV, merged_rows)
    print(f"Updated {REPO_CSV}")

    run_update_script()
    print("Ran update_HTML_files.py successfully")


if __name__ == "__main__":
    main()