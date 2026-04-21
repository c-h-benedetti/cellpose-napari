from cellpose_napari.widgets.training_widget import TrainingWidget

from autooptions import Options

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import napari


class CP3TrainingWidget(TrainingWidget):
    
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__(viewer)

    def getOptions(self):
        options = Options("NapariCellpose", "Training CP3")
        self.makeBaseOptions(options)
        self.addChoice("Model", "cyto3", [
            "cyto3", 
            "cyto2", 
            "cyto", 
            "nuclei",
            "tissuenet_cp3", 
            "livecell_cp3", 
            "yeast_PhC_cp3", 
            "yeast_BF_cp3", 
            "bact_phase_cp3", 
            "bact_fluor_cp3",
            "deepbacs_cp3",
            "cyto2_cp3"
        ])
        options.load()
        return options