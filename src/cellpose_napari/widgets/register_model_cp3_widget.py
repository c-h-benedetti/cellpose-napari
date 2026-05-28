from cellpose_napari.widgets.register_model_widget import RegisterModelWidget
from cellpose_napari.ressources import getLocalModelsJsonCP3

from autooptions import Options

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import napari


class CP3RegisterModelWidget(RegisterModelWidget):
    
    def __init__(self, viewer: "napari.viewer.Viewer"): # type: ignore
        super().__init__(viewer)

    def getOptions(self):
        options = Options("NapariCellpose", "Register CP3 Model")
        self.makeBaseOptions(options)
        options.load()
        return options
    
    def getLocalModelsJson(self):
        return getLocalModelsJsonCP3()