from cellpose_napari.widgets.batch_widget import BatchWidget

from autooptions import Options

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import napari


class CPSAMBatchWidget(BatchWidget):
    
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__(viewer)

    def getOptions(self):
        options = Options("NapariCellpose", "Batch CPSAM")
        self.makeBaseOptions(options)
        options.load()
        return options