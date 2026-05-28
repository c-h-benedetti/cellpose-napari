import random
import tifffile
from pathlib import Path


def list_tiff_files(folder):
    """Return the list of all .tif / .tiff files in the folder."""
    extensions = {".tif", ".tiff"}
    return sorted(p for p in folder.iterdir() if p.suffix.lower() in extensions)


def load_stack(path):
    """
    Load a TIFF stack and guarantee a 3D array (Z, Y, X).
    Raise a ValueError if the array is not 3D after loading.
    """
    stack = tifffile.imread(str(path))
    if stack.ndim != 3:
        raise ValueError(
            f"{path.name}: expected a 3D stack (Z, Y, X), "
            f"got shape={stack.shape}"
        )
    return stack  # shape: (Z, Y, X)


def sample_indices(axis_size, n):
    """
    Draw n unique random indices in [0, axis_size).
    If n >= axis_size, return all indices in random order.
    """
    n = min(n, axis_size)
    return random.sample(range(axis_size), n)


# ---------------------------------------------------------------------------
# Axis extraction
# ---------------------------------------------------------------------------

def extract_yx_slices(stack, n):
    """
    YX planes: slice along Z (fixed Z, return the YxX plane).
    Return a list of (z_index, slice_2d).
    """
    z_size = stack.shape[0]
    indices = sample_indices(z_size, n)
    return [(z, stack[z, :, :]) for z in indices]


def extract_zx_slices(stack, n):
    """
    ZX planes: slice along Y (fixed Y, return the ZxX plane).
    Return a list of (y_index, slice_2d).
    """
    y_size = stack.shape[1]
    indices = sample_indices(y_size, n)
    return [(y, stack[:, y, :]) for y in indices]


def extract_zy_slices(stack, n):
    """
    ZY planes: slice along X (fixed X, return the ZxY plane).
    Return a list of (x_index, slice_2d).
    """
    x_size = stack.shape[2]
    indices = sample_indices(x_size, n)
    return [(x, stack[:, :, x]) for x in indices]


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

def save_slice(
    slice_2d,
    output_dir,
    prefix,
    stack_stem,
    plane_index,
):
    """
    Save a 2D plane as TIFF in output_dir.
    File name: {prefix}_{stack_stem}_plane{plane_index:04d}.tif
    """
    filename = f"{prefix}_{stack_stem}_plane{plane_index:04d}.tif"
    dest = output_dir / filename
    tifffile.imwrite(str(dest), slice_2d)


def process_stack(
    path,
    output_dir,
    n_slices,
):
    """
    Load one stack and export the requested slices for each axis.

    Parameters
    ----------
    path       : path to the TIFF file
    output_dir : output folder
    n_slices   : dict with keys 'YX', 'ZX', 'ZY' and number of planes to sample
    """
    print(f"  Processing: {path.name}")

    try:
        stack = load_stack(path)
    except ValueError as e:
        print(f"    [SKIP] {e}")
        return

    stem = path.stem

    extractors = {
        "YX": extract_yx_slices,
        "ZX": extract_zx_slices,
        "ZY": extract_zy_slices,
    }

    for axis, extractor in extractors.items():
        n = n_slices.get(axis, 0)
        if n <= 0:
            continue

        slices = extractor(stack, n)
        for plane_index, slice_2d in slices:
            save_slice(slice_2d, output_dir, axis, stem, plane_index)

        print(f"    {axis}: {len(slices)} plane(s) exported")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # ------------------------------------------------------------------ #
    #  Parameters - edit here                                              #
    # ------------------------------------------------------------------ #
    input_folder  = Path("/home/clement/Downloads/2026-03-31-fabrice-yeasts/transfer_12331331_files_721d68f3/fero-yeasts")
    output_folder = input_folder / "sliced"

    n_slices = {
        "YX": 5, # number of Z planes to sample (top view)
        "ZX": 5, # number of Y planes to sample (frontal slice)
        "ZY": 5, # number of X planes to sample (sagittal slice)
    }
    # ------------------------------------------------------------------ #

    if not input_folder.exists():
        raise FileNotFoundError(f"Folder not found: {input_folder}")

    output_folder.mkdir(parents=True, exist_ok=True)

    tiff_files = list_tiff_files(input_folder)
    if not tiff_files:
        print(f"No TIFF file found in {input_folder}")
        return

    print(f"Stacks found: {len(tiff_files)}")
    print(f"Output      : {output_folder}\n")

    for tiff_path in tiff_files:
        process_stack(tiff_path, output_folder, n_slices)

    print("\nDone.")


if __name__ == "__main__":
    main()