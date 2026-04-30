from abc import ABC, abstractmethod
from pathlib import Path
import tifffile
import numpy as np
from skimage.measure import regionprops
from tqdm import tqdm

class CellPoseBaseTraining(ABC):
    def __init__(self, settings):
        self.training_folder = Path(settings["training_folder"])
        self.testing_folder = Path(settings["testing_folder"]) if settings["testing_folder"] is not None else None
        self.look_one_level_down = settings["look_one_level_down"]
        self.axes = settings["axes"]
        self.images_filter = settings["images_filter"]
        self.masks_filter = settings["masks_filter"]
        self.model_name = settings["model_name"]
        self.base_model_name = settings["base_model"]
        self.use_gpu = settings["use_gpu"]
        self.weight_decay = settings["weight_decay"]
        self.learning_rate = settings["learning_rate"]
        self.n_epochs = settings["n_epochs"]
        self.batch_size = settings["batch_size"]
        self.rescale = settings["rescale"]
        self.min_train_masks = settings["min_train_masks"]
        self.median_diameter = None
        self.model = None
        self.training_assessment = None
        self.default_base = None
        self.process_median_diameter()
        self.sanity_check()

    def sanity_check(self):
        if not self.training_folder.exists() or not self.training_folder.is_dir():
            raise ValueError(f"Training folder '{self.training_folder}' does not exist or is not a directory.")
        if self.testing_folder is not None and (not self.testing_folder.exists() or not self.testing_folder.is_dir()):
            raise ValueError(f"Testing folder '{self.testing_folder}' does not exist or is not a directory.")
        print("Sanity check passed successfully")

    def process_median_diameter(self):
        p = self.training_folder
        diameters = []
        for file in tqdm(p.iterdir(), desc="Processing median diameter"):
            if not file.is_file() or not str(file).endswith("_cp_masks.tif"):
                continue
            masks = tifffile.imread(file)
            for region in regionprops(masks):
                diameters.append(region.equivalent_diameter_area)
        diameters = sorted(diameters)
        self.median_diameter = diameters[len(diameters)//2] if diameters else None

    @abstractmethod
    def getBaseModelPath(self):
        raise Exception("Abstract method getBaseModelPath of class CellPoseBaseTraining called!")
    
    @abstractmethod
    def instanciate_model(self):
        raise Exception("Abstract method instanciate_model of class CellPoseBaseTraining called!")
    
    @abstractmethod
    def launch_training(self):
        raise Exception("Abstract method launch_training of class CellPoseBaseTraining called!")
    
    def run(self):
        self.instanciate_model()
        self.launch_training()