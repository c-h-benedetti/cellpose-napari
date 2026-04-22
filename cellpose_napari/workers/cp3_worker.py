from cellpose_napari.workers.cellpose_worker import CellPoseBaseWorker
from cellpose_napari.ressources import getLocalModelsJsonCP3

class CP3Worker(CellPoseBaseWorker):
    def __init__(self, ch_main, ch_secondary, model, diameter, anisotropy, min_size, cell_prob, flow_thr, flow_smooth, axes, use_gpu):
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
            axes,
            use_gpu
        )

    def get_json_models_path(self):
        return getLocalModelsJsonCP3()
    
    def instanciate_model(self):
        pass

    def run_model(self, im_data, do_3d):
        pass