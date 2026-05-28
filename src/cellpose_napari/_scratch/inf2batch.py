import argparse
import os
import shutil
import secrets
from pathlib import Path
 
 
def random_suffix(length: int) -> str:
    """Generate a random hex string of given length."""
    return secrets.token_hex(length // 2 + 1)[:length]
 
 
def find_pair_dirs(root: Path) -> list[tuple[Path, Path | None, Path | None]]:
    """
    Walk root recursively.
    Return list of (c1_path, c2_or_None, description_json_or_None)
    for every dir containing c1.tif.
    """
    pairs = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        filenames_set = set(filenames)
        if "c1.tif" in filenames_set:
            c1   = Path(dirpath) / "c1.tif"
            c2   = Path(dirpath) / "c2.tif"          if "c2.tif"           in filenames_set else None
            desc = Path(dirpath) / "description.json" if "description.json" in filenames_set else None
            pairs.append((c1, c2, desc))
    return pairs
 
 
def make_copies(
    c1: Path,
    c2: Path | None,
    desc: Path | None,
    n_copies: int,
    suffix_len: int,
    output_dir: Path | None,
    dry_run: bool,
) -> None:
    """
    Create n_copies of c1 (and c2 if present), each pair sharing the same suffix.
    Also copies description.json once, keeping its original name.
    """
    used_suffixes: set[str] = set()
 
    for _ in range(n_copies):
        # Guarantee uniqueness within this batch
        while True:
            suffix = random_suffix(suffix_len)
            if suffix not in used_suffixes:
                used_suffixes.add(suffix)
                break
 
        # Resolve destination directory
        if output_dir is not None:
            # Mirror the source directory structure under output_dir
            rel = c1.parent.relative_to(c1.parent.parts[0] if output_dir else Path("."))
            try:
                rel = c1.parent.relative_to(c1.parents[len(c1.parts) - len(output_dir.parts) - 1])
            except Exception:
                rel = Path(c1.parent.name)
            dest_dir = output_dir / rel
        else:
            dest_dir = c1.parent
 
        if not dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)
 
        # Build destination filenames
        c1_dest = dest_dir / f"c1-{suffix}.tif"
        action = f"[dry-run] " if dry_run else ""
 
        if dry_run:
            print(f"{action}{c1}  →  {c1_dest}")
        else:
            shutil.copy2(c1, c1_dest)
            print(f"{c1}  →  {c1_dest}")
 
        if c2 is not None:
            c2_dest = dest_dir / f"c2-{suffix}.tif"
            if dry_run:
                print(f"{action}{c2}  →  {c2_dest}")
            else:
                shutil.copy2(c2, c2_dest)
                print(f"{c2}  →  {c2_dest}")
 
    # Copy description.json once, name unchanged
    if desc is not None:
        if output_dir is not None:
            try:
                rel = desc.parent.relative_to(desc.parents[len(desc.parts) - len(output_dir.parts) - 1])
            except Exception:
                rel = Path(desc.parent.name)
            desc_dest_dir = output_dir / rel
        else:
            desc_dest_dir = desc.parent
 
        desc_dest = desc_dest_dir / "description.json"
        if dry_run:
            print(f"[dry-run] {desc}  →  {desc_dest}  (single copy)")
        else:
            if not dry_run:
                desc_dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(desc, desc_dest)
            print(f"{desc}  →  {desc_dest}  (single copy)")
 
 
def run(
    input_folder: Path,
    n_copies: int,
    suffix_len: int,
    output_dir: Path | None,
    dry_run: bool,
) -> None:
    if not input_folder.exists():
        raise FileNotFoundError(f"Input folder not found: {input_folder}")
 
    pairs = find_pair_dirs(input_folder)
 
    if not pairs:
        print("No directories containing c1.tif were found.")
        return
 
    print(f"Found {len(pairs)} directory/ies with c1.tif.\n")
 
    total_copies = 0
    for c1, c2, desc in pairs:
        has_c2  = c2   is not None
        has_desc = desc is not None
        print(f"── {c1.parent}  [c2={'yes' if has_c2 else 'no'}  desc={'yes' if has_desc else 'no'}]")
        make_copies(c1, c2, desc, n_copies, suffix_len, output_dir, dry_run)
        total_copies += n_copies * (2 if has_c2 else 1) + (1 if has_desc else 0)
        print()
 
    label = "[dry-run] " if dry_run else ""
    print(f"{label}Done: {total_copies} file(s) would be created." if dry_run
          else f"Done: {total_copies} file(s) created.")


def main():
    run(
        input_folder=Path("/home/clement/Desktop/cellpose_napari_wd/inference_datasets"),
        n_copies=3,
        suffix_len=5,
        output_dir=Path("/home/clement/Desktop/cellpose_napari_wd/batch_datasets"),
        dry_run=False
    )


if __name__ == "__main__":
    main()