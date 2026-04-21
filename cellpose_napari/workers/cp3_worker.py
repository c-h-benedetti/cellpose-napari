from cellpose_napari.workers import CellPoseWorker
from cellpose_napari.ressources import getLocalModelsJsonCP3

class CP3Worker(CellPoseWorker):
    def __init__(self, ch_main, ch_secondary, model, diameter, anisotropy, min_size, cell_prob, flow_thr, flow_smooth, axes):
        super().__init__(
            ch_main, 
            ch_secondary, 
            model, 
            diameter, 
            anisotropy, 
            min_size, 
            cell_prob, 
            flow_thr, 
            flow_smooth, 
            axes
        )

    def get_json_models_path(self):
        return getLocalModelsJsonCP3()