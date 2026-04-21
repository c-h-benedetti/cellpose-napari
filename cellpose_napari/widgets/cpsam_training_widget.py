from cellpose_napari.widgets.training_widget import TrainingWidget

from autooptions import Options

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import napari


class CPSAMTrainingWidget(TrainingWidget):
    
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__(viewer)

    def getOptions(self):
        options = Options("NapariCellpose", "Training CPSAM")
        self.makeBaseOptions(options)
        options.load()
        return options