## -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 23:24:00 2024

@author: Daniel
"""
import imageio
from os import listdir
from os.path import isfile, join
from pathlib import Path

def main(name, chapter, display_name=None):
    """
    name: folder name under gifs_chapter/chapter_X/
    display_name: final GIF filename in animations/ (without .gif)
    """
    images = []

    source_name = str(name).strip()
    output_name = str(display_name).strip() if display_name else source_name

    repo_root = Path(".").resolve()
    imagePath = repo_root / "gifs_chapter" / f"chapter_{chapter}" / source_name / f"{source_name}_images"
    gifDir = repo_root / "animations"
    gifDir.mkdir(parents=True, exist_ok=True)
    gifPath = gifDir / f"{output_name}.gif"

    fileNames = [f for f in listdir(imagePath) if isfile(join(imagePath, f))]
    fileNames.sort()

    for fileName in fileNames:
        print(fileName)
        images.append(imageio.imread(imagePath / fileName))

    imageio.mimsave(gifPath, images)
    print(f"Saved: {gifPath}")