from cellpose_napari.widgets.training_widget import TrainingWidget
from cellpose_napari.ressources import (
    getBaseModelsCP3,
    getLocalModelsJsonCP3
)
import json
from autooptions import Options
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import napari


class CP3TrainingWidget(TrainingWidget):
    
    def __init__(self, viewer: "napari.viewer.Viewer"): # type: ignore
        super().__init__(viewer)

    def getOptions(self):
        options = Options("NapariCellpose", "Training CP3")
        self.makeBaseOptions(options)
        options.addInt("Main channel", 0)
        options.addInt("Secondary channel", 0, optional=(True, False))
        options.addBool("Use SGD?", value=False)
        options.load()
        return options
    
    def getCellPoseModels(self):
        base_models = getBaseModelsCP3()
        local_models_json = getLocalModelsJsonCP3()
        local_models = []
        if local_models_json.exists():
            with open(local_models_json, 'r') as f:
                found_models = json.load(f)
                local_models = ["//" + model for model in found_models.keys()]
        return base_models + local_models
    
    def captureData(self):
        data = super().captureData()
        data["use_sgd"] = self.options.get("Use SGD?")
        data["main_channel"] = self.options.get("Main channel")
        data["secondary_channel"] = self.options.get("Secondary channel")
        return data