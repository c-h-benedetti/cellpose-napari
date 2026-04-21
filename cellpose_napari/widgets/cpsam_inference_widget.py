from cellpose_napari.widgets.inference_widget import InferenceWidget
from cellpose_napari.ressources import (
    getBaseModelsCPSAM,
    getLocalModelsJsonCPSAM
)

import json

from autooptions import Options

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import napari

class CPSAMInferenceWidget(InferenceWidget):
    
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__(viewer)

    def getOptions(self):
        options = Options("NapariCellpose", "Inference CPSAM")
        self.makeBaseOptions(options)
        options.load()
        return options
    
    def getCellPoseModels(self):
        base_models = getBaseModelsCPSAM()
        local_models_json = getLocalModelsJsonCPSAM()
        local_models = []
        if local_models_json.exists():
            with open(local_models_json, 'r') as f:
                found_models = json.load(f)
                local_models = ["//" + model for model in found_models.keys()]
        return base_models + local_models