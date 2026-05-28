from cellpose_napari.widgets.inference_widget import InferenceWidget
from cellpose_napari.ressources import (
    getBaseModelsCP3,
    getLocalModelsJsonCP3
)

import json

from autooptions import Options

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import napari

class CP3InferenceWidget(InferenceWidget):
    
    def __init__(self, viewer: "napari.viewer.Viewer"): # type: ignore
        super().__init__(viewer)

    def getOptions(self):
        options = Options("NapariCellpose", "Inference CP3")
        self.makeBaseOptions(options)
        options.load()
        return options
