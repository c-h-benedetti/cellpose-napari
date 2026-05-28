from cellpose_napari.widgets.batch_widget import BatchWidget
from autooptions import Options

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import napari


class CP3BatchWidget(BatchWidget):
    
    def __init__(self, viewer: "napari.viewer.Viewer"): # type: ignore
        super().__init__(viewer)

    def getOptions(self):
        options = Options("NapariCellpose", "Batch CP3")
        self.makeBaseOptions(options)
        options.load()
        return options
    