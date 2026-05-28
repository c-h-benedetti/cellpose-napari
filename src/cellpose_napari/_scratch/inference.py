import tifffile
from pathlib import Path
import json
from cellpose_napari import CellPoseInference, ImageUtils
import xarray as xr
import shutil
from cellpose_napari._scratch.tools import probe_folder, remove_root


if __name__ == "__main__":
    dataset_root = Path("/home/clement/Desktop/cellpose_napari_wd/inference_datasets")
    output_root  = Path("/home/clement/Desktop/cellpose_napari_wd/inference_output")
    paths        = probe_folder(dataset_root)

    shutil.rmtree(output_root, ignore_errors=True)
    output_root.mkdir(parents=True, exist_ok=True)

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
        
        min_size = 20
        cell_prob = 0.0
        flow_thr = 0.4
        flow_smooth = 0

        c1 = xr.DataArray(c1, dims=list(axes))
        c1 = ImageUtils.ensureAxes(c1)
        c2 = xr.DataArray(c2, dims=list(axes)) if c2 is not None else None
        c2 = ImageUtils.ensureAxes(c2) if c2 is not None else None

        worker = CellPoseInference( # using default model
            ch_main=c1,
            ch_secondary=c2,
            diameter=diameter,
            anisotropy=anisotropy,
            min_size=min_size,
            cell_prob=cell_prob,
            flow_thr=flow_thr,
            flow_smooth=flow_smooth,
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