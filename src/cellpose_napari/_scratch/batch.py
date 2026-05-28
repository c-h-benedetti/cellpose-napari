from cellpose_napari import CellPoseBatchWorker
import os
import shutil
from pathlib import Path
import json
from cellpose_napari._scratch.tools import probe_folder, remove_root

dataset_root = Path("/home/clement/Desktop/cellpose_napari_wd/batch_datasets")
output_root  = Path("/home/clement/Desktop/cellpose_napari_wd/batch_output")
paths        = probe_folder(dataset_root)

shutil.rmtree(output_root, ignore_errors=True)
output_root.mkdir(parents=True, exist_ok=True)

for path in paths:
    print(f">>> Processing {path}")
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

    min_size = 20
    cell_prob = 0.0
    flow_thr = 0.4
    flow_smooth = 0

    input_folder = path
    output_folder = output_root / remove_root(path, dataset_root)
    main_channel_prefix = "c1"
    secondary_channel_prefix = "c2" if (path / "c2.tif").is_file() else None
    pixel_size_yx = 1.0
    pixel_size_z = anisotropy
    model = 'cyto3'
    median_diameter = diameter
    use_gpu = True
    cell_prob_threshold = cell_prob
    flow_threshold = flow_thr
    flow_smoothing = flow_smooth
    segmentation_prefix = "seg_"

    wpbw = CellPoseBatchWorker(
        input_folder, 
        output_folder, 
        main_channel_prefix, 
        secondary_channel_prefix, 
        axes, 
        pixel_size_yx, 
        pixel_size_z, 
        model, 
        median_diameter, 
        min_size, 
        use_gpu, 
        cell_prob_threshold, 
        flow_threshold, 
        flow_smoothing, 
        segmentation_prefix
    )

    for t in wpbw.run():
        pass
