from pathlib import Path
import json
from abc import ABC, abstractmethod

class CellPoseWorker(ABC):
    def __init__(self, ch_main, ch_secondary, model, diameter, anisotropy, min_size, cell_prob, flow_thr, flow_smooth, axes):
        self.main_channel = ch_main
        self.secondary_channel = ch_secondary
        self.model = self.find_model(model)
        self.diameter = diameter
        self.anisotropy = anisotropy
        self.min_object_size = min_size
        self.cell_prob_threshold = cell_prob
        self.flow_threshold = flow_thr
        self.flow_smooth = flow_smooth
        self.axes = axes
        self.sanity_check()

    def sanity_check(self):
        if self.main_channel is None:
            raise ValueError("Main channel cannot be None")
        if self.secondary_channel is not None and self.secondary_channel.shape != self.main_channel.shape:
            raise ValueError("Secondary channel must have the same shape as the main channel")
        if self.model is None:
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
        
    @abstractmethod
    def run(self):
        raise NotImplementedError("Subclasses should implement this method to run the worker.")
    
    @abstractmethod
    def instanciate_model(self):
        raise NotImplementedError("Subclasses should implement this method to instanciate the model.")