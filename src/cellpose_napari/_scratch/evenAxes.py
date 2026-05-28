from pathlib import Path

import numpy as np
import tifffile


def process(folder: Path, dry_run: bool) -> None:
    masks = sorted(folder.rglob("*_cp_masks*"))

    if not masks:
        print("No _cp_masks files found.")
        return

    print(f"Found {len(masks)} file(s).\n")

    for path in masks:
        arr = tifffile.imread(path)
        new_arr = arr[..., np.newaxis]
        print(f"{path}")
        print(f"  {arr.shape} {arr.dtype}  →  {new_arr.shape}")
        if not dry_run:
            tifffile.imwrite(path, new_arr)

    print(f"\n{'[dry-run] ' if dry_run else ''}Done: {len(masks)} file(s) processed.")


def main():
    process(
        Path("/home/clement/Documents/projects/2219-intensity-membrane/augmented/training"), 
        False
    )
    process(
        Path("/home/clement/Documents/projects/2219-intensity-membrane/augmented/testing"), 
        False
    )


if __name__ == "__main__":
    main()