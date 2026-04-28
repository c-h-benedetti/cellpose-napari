from abc import ABC, abstractmethod
from datetime import datetime

from cellpose_napari.widgets.widget import Widget

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import napari

class TrainingWidget(Widget):
    
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__(viewer)

    def makeBaseOptions(self, options):
        models = self.getCellPoseModels()
        options.addFolder("Training images")
        options.addFolder("Testing images", optional=(True, False))
        options.addBool("Look one level down?", value=False)
        options.addChoice("Axes", value="YX", choices=["YX", "CYX", "ZYX", "CZYX", "ZCYX"])
        options.addStr("Images filter", value="_img", optional=(True, False))
        options.addStr("Masks filter", value="_cp_masks")
        options.addChoice("Base model", value=models[0], choices=models, optional=(True, True))
        options.addStr("Model name", value=self.generate_timestamp_version(), transient=True)
        options.addBool("Use GPU?", value=True)
        options.addFloat("Weight decay", value=0.1)
        options.addFloat("Learning rate", value=0.001)
        options.addInt("Number of epochs", value=500)
        options.addInt("Batch size", value=16)
        options.addBool("Rescale?", value=True)
        options.addInt("Min objects per image", value=1)

    def generate_timestamp_version(self):
        return datetime.now().strftime("%Y-%m-%d_%H-%M")

    @abstractmethod
    def getCellPoseModels(self):
        raise Exception("Abstract method getCellPoseModels of class InferenceWidget called!")
    
    @abstractmethod
    def makeOperation(self):
        raise Exception("Abstract method makeOperation of class TrainingWidget called!")
    
    def captureData(self):
        return {
            "training_folder": self.options.value("Training images"),
            "testing_folder": self.options.value("Testing images"),
            "look_one_level_down": self.options.value("Look one level down?"),
            "axes": self.options.value("Axes"),
            "images_filter": self.options.value("Images filter"),
            "masks_filter": self.options.value("Masks filter"),
            "model_name": self.options.value("Model name"),
            "base_model": self.options.value("Base model"),
            "use_gpu": self.options.value("Use GPU?"),
            "weight_decay": self.options.value("Weight decay"),
            "learning_rate": self.options.value("Learning rate"),
            "n_epochs": self.options.value("Number of epochs"),
            "batch_size": self.options.value("Batch size"),
            "rescale": self.options.value("Rescale?"),
            "min_train_masks": self.options.value("Min objects per image")
        }