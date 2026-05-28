from abc import ABC, abstractmethod
from pathlib import Path
import tifffile
from skimage.measure import regionprops
from tqdm import tqdm
import numpy as np
import os
import matplotlib
matplotlib.use("Agg")  # no GUI
import matplotlib.pyplot as plt
import xarray as xr


class CellPoseBaseTraining(ABC):
    def __init__(self, settings):
        self.training_folder = Path(settings["training_folder"])
        self.testing_folder = Path(settings["testing_folder"]) if settings["testing_folder"] is not None else None
        self.look_one_level_down = settings["look_one_level_down"]
        self.images_filter = settings["images_filter"]
        self.masks_filter = settings["masks_filter"]
        self.model_name = settings["model_name"]
        self.base_model_name = settings["base_model"]
        self.use_gpu = settings["use_gpu"]
        self.axes = settings["axes"]
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
            masks = xr.DataArray(masks, dims=list(self.axes))
            if 'C' in self.axes: # drop the axis
                masks = masks.isel(C=0)
            for region in regionprops(masks.values):
                diameters.append(region.equivalent_diameter_area)
        diameters = sorted(diameters)
        self.median_diameter = diameters[len(diameters)//2] if diameters else None
        print(f"Estimated median diameter: {self.median_diameter:.2f} pixels")

    @abstractmethod
    def getBaseModelPath(self):
        raise Exception("Abstract method getBaseModelPath of class CellPoseBaseTraining called!")
    
    @abstractmethod
    def instanciate_model(self):
        raise Exception("Abstract method instanciate_model of class CellPoseBaseTraining called!")
    
    @abstractmethod
    def launch_training(self):
        raise Exception("Abstract method launch_training of class CellPoseBaseTraining called!")
    
    @abstractmethod
    def formatDataPair(self, images, masks):
        raise Exception("Abstract method formatDataPair of class CellPoseBaseTraining called!")
    
    def run(self):
        os.chdir(self.training_folder.parent)
        self.instanciate_model()
        self.launch_training()

    def plot_losses(self, model_path, train_losses, test_losses):
        epochs = np.arange(1, len(train_losses) + 1)
 
        test_mask = test_losses != 0
        test_epochs = epochs[test_mask]
        test_vals   = test_losses[test_mask]
        
        fig, ax = plt.subplots(figsize=(9, 5))
        
        ax.plot(epochs, train_losses, marker="o", markersize=4, linewidth=1.8,
                color="#2d6a9f", label="Train loss")
        ax.plot(test_epochs, test_vals, marker="s", markersize=6, linewidth=1.8,
                linestyle="--", color="#c0392b", label="Test loss")
        
        ax.set_xlabel("Epoch", fontsize=12)
        ax.set_ylabel("Loss", fontsize=12)
        ax.set_title("Training curves", fontsize=14)
        ax.legend(fontsize=11)
        ax.locator_params(axis='x', nbins=10)
        ax.grid(True, linestyle="--", alpha=0.4)
        fig.tight_layout()
        
        out = Path(model_path).parent / "training_curves.png"
        fig.savefig(out, dpi=150)
        plt.close(fig)
        print(f"Saved → {out}")