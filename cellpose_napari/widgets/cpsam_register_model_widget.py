from cellpose_napari.widgets.register_model_widget import RegisterModelWidget
from cellpose_napari.ressources import getLocalModelsJsonCPSAM

from autooptions import Options

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import napari


class CPSAMRegisterModelWidget(RegisterModelWidget):
    
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__(viewer)

    def getOptions(self):
        options = Options("NapariCellpose", "Register CPSAM Model")
        self.makeBaseOptions(options)
        options.load()
        return options
    
    def getLocalModelsJson(self):
        return getLocalModelsJsonCPSAM()