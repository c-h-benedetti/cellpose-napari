import tifffile
from pathlib import Path
import json
from cellpose_napari import CellPoseWorker

def is_data(folder_path):
    if not folder_path.is_dir():
        return False
    if "c1.tif" not in [f.name for f in folder_path.iterdir() if f.is_file()]:
        return False
    return True

def recursive_folder_exploration(root, folders):
    if not root.is_dir():
        return
    if is_data(root):
        folders.append(root)
    for child in root.iterdir():
        recursive_folder_exploration(child, folders)

def probe_folder(root_folder):
    folders = []
    recursive_folder_exploration(root_folder, folders)
    return folders

def remove_root(p1, p2):
    # Removes the parts that both folders have in common in p2
    p1_parts = p1.parts
    p2_parts = p2.parts
    kept = []
    is_root = True
    
    for i, p in enumerate(p2_parts):
        if not is_root:
            kept.append(p)
            continue
        if i >= len(p1_parts) or p != p1_parts[i]:
            is_root = False
            kept.append(p)
    return Path(*kept)

dataset_root = Path("/home/clement/Desktop/cellpose_napari_wd/datasets")
output_root  = Path("/home/clement/Desktop/cellpose_napari_wd/outputs")
paths = probe_folder(dataset_root)

for path in paths:
    print(f">>> Processing {path}")
    c1_path = path / "c1.tif"
    c2_path = path / "c2.tif"
    description_path = path / "description.json"
    if not description_path.is_file():
        print(f"Missing description.json in {path}")
        continue
    with open(description_path) as f:
        description = json.load(f)
    diameter = description.get("diameter", None)
    anisotropy = description.get("anisotropy", None)
    axes = description.get("axes", None)
    if diameter is None or anisotropy is None or axes is None:
        print(f"Missing diameter, anisotropy or axes in description.json in {path}")
        continue
    c1 = tifffile.imread(c1_path)
    c2 = tifffile.imread(c2_path) if c2_path.is_file() else None
    model = 'cpsam'
    min_size = 20
    cell_prob = 0.0
    flow_thr = 0.4
    flow_smooth = 0.0

    worker = CellPoseWorker(
        ch_main=c1,
        ch_secondary=c2,
        model=model,
        diameter=diameter,
        anisotropy=anisotropy,
        min_size=min_size,
        cell_prob=cell_prob,
        flow_thr=flow_thr,
        flow_smooth=flow_smooth,
        axes=axes,
        use_gpu=True
    )

    for t in worker.run():
        pass

    output_path = output_root / remove_root(dataset_root, path)
    output_path.mkdir(parents=True, exist_ok=True)
    
    tifffile.imwrite(
        output_path / "result.tif", 
        worker.output_buffer,
        imagej=True
    )
    print("\n\n\n")

print("Done.")