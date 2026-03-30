from pathlib import Path
import pandas as pd

ANIM_DIR = Path("animations")
CSV_PATH = Path("gif_data.csv")

def strip_gif_suffix(s: str) -> str:
    s = str(s).strip()
    if s.lower().endswith(".gif"):
        s = s[:-4]
    return s

def drive_variant(s: str) -> str:
    """
    Approximate the common Google Drive / Windows apostrophe rewrite.
    Keep everything else the same.
    """
    s = strip_gif_suffix(s)
    s = s.replace("'", "_").replace("’", "_")
    return s

df = pd.read_csv(CSV_PATH, keep_default_na=False)

# exact filenames that actually exist in animations/
existing_files = {p.name for p in ANIM_DIR.glob("*.gif")}

matched = 0
unmatched = []

for i, row in df.iterrows():
    name = strip_gif_suffix(row["name"])
    display_name = strip_gif_suffix(row["display_name"])

    candidates = [
        f"{display_name}.gif",          # prefer display_name
        f"{name}.gif",                  # fallback to name
        f"{drive_variant(display_name)}.gif",  # display_name with apostrophe->underscore
        f"{drive_variant(name)}.gif",          # name with apostrophe->underscore
    ]

    chosen = ""
    for candidate in candidates:
        if candidate in existing_files:
            chosen = candidate
            break

    if chosen:
        df.at[i, "file_name"] = chosen
        matched += 1
        print(f'MATCH: {display_name} -> {chosen}')
    else:
        df.at[i, "file_name"] = ""
        unmatched.append((display_name, name))

df.to_csv(CSV_PATH, index=False, encoding="utf-8")

print(f"\nMatched {matched} rows.")
print(f"Unmatched {len(unmatched)} rows.")

if unmatched:
    print("\nUnmatched rows:")
    for display_name, name in unmatched:
        print(f"  display_name={display_name!r} | name={name!r}")