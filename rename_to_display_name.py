import pandas as pd
from pathlib import Path
import re

anim_dir = Path("animations")
df = pd.read_csv("gif_data.csv", keep_default_na=False)

def safe_filename(name: str) -> str:
    name = str(name).strip()
    if name.lower().endswith(".gif"):
        name = name[:-4]
    name = re.sub(r'[\\/:*?"<>|]', '-', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

renamed = 0
missing = []

for _, row in df.iterrows():
    old_name = str(row["name"]).strip()
    new_name = safe_filename(row["display_name"])

    if old_name.lower().endswith(".gif"):
        old_name = old_name[:-4]

    old_path = anim_dir / f"{old_name}.gif"
    new_path = anim_dir / f"{new_name}.gif"

    if old_path.exists():
        if old_path != new_path:
            print(f'Renaming: "{old_path.name}" -> "{new_path.name}"')
            old_path.rename(new_path)
            renamed += 1
    elif new_path.exists():
        print(f'Already correct: "{new_path.name}"')
    else:
        missing.append(old_name)

print(f"\nRenamed {renamed} files.")
if missing:
    print("\nMissing files:")
    for name in missing:
        print(f"  {name}.gif")