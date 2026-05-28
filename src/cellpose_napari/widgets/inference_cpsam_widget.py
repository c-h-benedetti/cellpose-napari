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
    
    def __init__(self, viewer: "napari.viewer.Viewer"): # type: ignore
        super().__init__(viewer)

    def getOptions(self):
        options = Options("NapariCellpose", "Inference CPSAM")
        self.makeBaseOptions(options)
        options.load()
        return options
    