from cellpose_napari import CellPoseWorker
import re
import tifffile
import numpy as np
from pathlib import Path

class CPBatchWorker(object):
    def __init__(self, input_folder, output_folder, main_channel_prefix, secondary_channel_prefix, axes, pixel_size_yx, pixel_size_z, model, median_diameter, min_size, use_gpu, cell_prob_threshold, flow_threshold, flow_smoothing, segmentation_prefix):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.main_channel_prefix = main_channel_prefix
        self.secondary_channel_prefix = secondary_channel_prefix
        self.axes = axes
        self.pixel_size_yx = pixel_size_yx
        self.pixel_size_z = pixel_size_z
        self.model = model
        self.median_diameter = median_diameter
        self.min_size = min_size
        self.use_gpu = use_gpu
        self.cell_prob_threshold = cell_prob_threshold
        self.flow_threshold = flow_threshold
        self.flow_smoothing = flow_smoothing
        self.segmentation_prefix = segmentation_prefix

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
        worker = CellPoseWorker(
            ch_main=ch_main,
            ch_secondary=ch_secondary,
            model=self.model,
            diameter=self.median_diameter,
            anisotropy=anisotropy,
            min_size=self.min_size,
            cell_prob=self.cell_prob_threshold,
            flow_thr=self.flow_threshold,
            flow_smooth=self.flow_smoothing,
            axes=self.axes,
            use_gpu=self.use_gpu,
        )
        return worker

    def run(self, callback=None):
        pairs = self.gather_files()
        total = len(pairs)
        worker = None
        for idx, (main_file, secondary_file) in enumerate(pairs):
            print(f"Processing file {idx+1}/{total}: {main_file.name}")
            ch_main = tifffile.imread(main_file)
            ch_secondary = tifffile.imread(secondary_file) if secondary_file is not None else None
            if worker is None:
                worker = self.instanciate_worker(ch_main, ch_secondary)
            else:
                worker.set_images(ch_main, ch_secondary)
            worker.run()
            output = worker.output_buffer
            output_path = Path(self.output_folder) / (self.segmentation_prefix + main_file.name)
            tifffile.imwrite(output_path, output.astype(np.uint16))
            if callback is not None:
                callback(idx+1, total)