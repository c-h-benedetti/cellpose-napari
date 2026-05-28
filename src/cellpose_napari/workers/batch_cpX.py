from cellpose_napari import CellPoseInference
import tifffile
import numpy as np
from pathlib import Path
import xarray as xr

from cellpose_napari.im_utils import ImageUtils

class CPBatchWorker(object):
    def __init__(self, input_folder, output_folder, main_channel_prefix, secondary_channel_prefix, axes, pixel_size_yx, pixel_size_z, model, median_diameter, min_size, use_gpu, cell_prob_threshold, flow_threshold, flow_smoothing, segmentation_prefix):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.main_channel_prefix = main_channel_prefix
        self.secondary_channel_prefix = secondary_channel_prefix
        self.pixel_size_yx = pixel_size_yx
        self.pixel_size_z = pixel_size_z
        self.model = model
        self.median_diameter = median_diameter
        self.min_size = min_size
        self.use_gpu = use_gpu
        self.axes = axes
        self.cell_prob_threshold = cell_prob_threshold
        self.flow_threshold = flow_threshold
        self.flow_smoothing = flow_smoothing
        self.segmentation_prefix = segmentation_prefix
        self.pairs = self.gather_files()

    def get_n_items(self):
        return len(self.pairs)

    def gather_files(self):
        input_path = Path(self.input_folder)
        files = [f for f in input_path.iterdir() if f.suffix.lower() in ['.tif', '.tiff']]
        main_channel_files = sorted([f for f in files if f.name.startswith(self.main_channel_prefix)])
        
        if self.secondary_channel_prefix is None:
            return [(main_file, None) for main_file in main_channel_files]
        
        secondary_channel_files = []
        for main_file in main_channel_files:
            secondary_file = input_path / (self.secondary_channel_prefix + main_file.name[len(self.main_channel_prefix):])
            if secondary_file.exists():
                secondary_channel_files.append(secondary_file)
            else:
                secondary_channel_files.append(None)

        pairs = list(zip(main_channel_files, secondary_channel_files))
        pairs = [pair for pair in pairs if pair[1] is not None]
        return pairs

    def instanciate_worker(self, ch_main, ch_secondary):
        anisotropy = 1.0
        if 'Z' in self.axes.upper() and self.pixel_size_z is not None and self.pixel_size_yx is not None:
            anisotropy = self.pixel_size_z / self.pixel_size_yx
        worker = CellPoseInference(
            ch_main=ch_main,
            ch_secondary=ch_secondary,
            model=self.model,
            diameter=self.median_diameter,
            anisotropy=anisotropy,
            min_size=self.min_size,
            cell_prob=self.cell_prob_threshold,
            flow_thr=self.flow_threshold,
            flow_smooth=self.flow_smoothing,
            use_gpu=self.use_gpu,
        )
        return worker
    
    def open_img(self, path):
        if path is None:
            return None
        img = tifffile.imread(path)
        img = xr.DataArray(img, dims=list(self.axes))
        img = ImageUtils.ensureAxes(img)
        return img
    
    def makeNewName(self, oldName):
        main_prefix = self.main_channel_prefix
        return self.segmentation_prefix + oldName[len(main_prefix):] # remove main prefix

    def run(self):
        total = len(self.pairs)
        worker = None
        for idx, (main_file, secondary_file) in enumerate(self.pairs):
            print(f"Processing file {idx+1}/{total}: {main_file.name}")
            ch_main = self.open_img(main_file)
            ch_secondary = self.open_img(secondary_file)
            if worker is None:
                worker = self.instanciate_worker(ch_main, ch_secondary)
            else:
                worker.set_images(ch_main, ch_secondary)
            list(worker.run()) # consume generator
            output = worker.output_buffer
            if output is None:
                print(f"Warning: no output for file {main_file.name}")
                continue
            output = ImageUtils.removeExtraAxes(output, self.axes)
            new_name = self.makeNewName(main_file.name)
            output_path = Path(self.output_folder) / new_name
            tifffile.imwrite(output_path, output, imagej=True)
            yield idx+1