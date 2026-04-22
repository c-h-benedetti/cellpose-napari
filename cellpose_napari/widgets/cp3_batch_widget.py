from cellpose_napari.widgets.batch_widget import BatchWidget
from cellpose_napari.ressources import (
    getBaseModelsCP3,
    getLocalModelsJsonCP3
)
import json

from autooptions import Options

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import napari


class CP3BatchWidget(BatchWidget):
    
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__(viewer)

    def getOptions(self):
        options = Options("NapariCellpose", "Batch CP3")
        self.makeBaseOptions(options)
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