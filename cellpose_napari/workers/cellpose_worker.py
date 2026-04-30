from pathlib import Path
import json
import numpy as np
from abc import ABC, abstractmethod
from tqdm import tqdm

class CellPoseBaseWorker(ABC):
    def __init__(self, ch_main, ch_secondary, model, diameter, anisotropy, min_size, cell_prob, flow_thr, flow_smooth, axes, use_gpu):
        self.main_channel = ch_main
        self.secondary_channel = ch_secondary
        self.model_name = self.find_model(model)
        self.diameter = diameter
        self.anisotropy = anisotropy
        self.min_object_size = min_size
        self.cell_prob_threshold = cell_prob
        self.flow_threshold = flow_thr
        self.flow_smooth = flow_smooth
        self.axes = axes
        self.use_gpu = use_gpu
        self.model = None
        self.output_buffer = None
        self.sanity_check()
        self.instanciate_model()

    def get_n_time_points(self):
        if 'T' in self.axes.upper():
            return self.main_channel.shape[self.axes.upper().index('T')]
        else:
            return 1

    def set_images(self, ch_main, ch_secondary=None):
        self.main_channel = ch_main
        self.secondary_channel = ch_secondary
        self.sanity_check()

    def sanity_check(self):
        if self.main_channel is None:
            raise ValueError("Main channel cannot be None")
        if self.secondary_channel is not None and self.secondary_channel.shape != self.main_channel.shape:
            raise ValueError("Secondary channel must have the same shape as the main channel")
        if self.model_name is None:
            raise ValueError("Model cannot be None")
        if self.diameter <= 0:
            raise ValueError("Diameter must be greater than 0")
        if self.anisotropy < 1.0:
            raise ValueError("Anisotropy must be greater than or equal to 1.0")
        if self.min_object_size <= 0:
            raise ValueError("Minimum object size must be greater than 0")
        if not (0 <= self.cell_prob_threshold <= 1):
            raise ValueError("Cell probability threshold must be between 0 and 1")
        if not (0 <= self.flow_threshold <= 1):
            raise ValueError("Flow threshold must be between 0 and 1")
        if self.flow_smooth < 0:
            raise ValueError("Flow smooth must be non-negative")
        print("Sanity check passed successfully")

    @abstractmethod
    def get_json_models_path(self):
        raise NotImplementedError("Subclasses should implement this method to return the path to the local models JSON file.")

    def find_model(self, model):
        if not model.startswith("//"):
            return model
        else:
            local_models_json = self.get_json_models_path()
            f = open(local_models_json)
            data = json.load(f)
            model_path = data.get(model[2:], None)
            if model_path is None:
                raise ValueError(f"Model {model} not found in {local_models_json}")
            p = Path(model_path)
            if not p.is_file():
                raise ValueError(f"Model path {model_path} does not exist")
            return model_path
    
    def apply_prefilter(self, im_data):
        return im_data

    def run(self):
        do_3d = 'Z' in self.axes.upper()
        main_channel = self.to_tzyx(self.main_channel, self.axes)
        secondary_channel = self.to_tzyx(self.secondary_channel, self.axes) if self.secondary_channel is not None else None
        self.output_buffer = np.zeros_like(main_channel, dtype=np.uint16)
        
        for t in tqdm(range(main_channel.shape[0]), desc="Processing time points"):
            if secondary_channel is not None:
                image = np.stack([main_channel[t], secondary_channel[t]], axis=0)
            else:
                image = main_channel[t]
                image = np.expand_dims(image, axis=0) # add channel axis for consistency, shape is now CZYX
            # shape of 'image' == CZYX from this point
            self.output_buffer[t] = self.run_model(image, do_3d)
            yield t+1
        
        # Back to the original shape
        self.output_buffer = self.to_original_axes(self.output_buffer, self.axes)
    
    @abstractmethod
    def run_model(self, im_data, do_3d):
        raise NotImplementedError("Subclasses should implement this method to run the model.")

    @abstractmethod
    def instanciate_model(self):
        raise NotImplementedError("Subclasses should implement this method to instanciate the model.")
    
    def to_tzyx(self, arr, axes):
        axes = [a.upper() for a in axes]

        if len(axes) != arr.ndim:
            raise ValueError(f"Axes length {len(axes)} does not match array ndim {arr.ndim}")
        
        if len(set(axes)) != len(axes):
            raise ValueError(f"Duplicate axes: {axes}")
        
        unknown = set(axes) - {'Z', 'T', 'Y', 'X'}
        if unknown:
            raise ValueError(f"Unknown axes: {unknown}")

        # Insert missing axes as size-1 dimensions
        target = ['T', 'Z', 'Y', 'X']
        for ax in target:
            if ax not in axes:
                arr = np.expand_dims(arr, axis=0)
                axes = [ax] + axes

        current_order = [axes.index(ax) for ax in target]
        arr = np.transpose(arr, current_order)

        return arr
    
    def to_original_axes(self, arr, target_axes):
        target_axes = [a.upper() for a in target_axes]
        current_axes = ['T', 'Z', 'Y', 'X']
        current_order = []
        index = 0
        # Remove axes that were not originally present
        for ax in current_axes:
            if ax not in target_axes:
                arr = np.squeeze(arr, axis=index)
            else:
                current_order.append(index)
                index += 1
                
        # Transpose back to original order
        arr = np.transpose(arr, current_order)
        return arr