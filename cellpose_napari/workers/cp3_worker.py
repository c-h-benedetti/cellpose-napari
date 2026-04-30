from cellpose_napari.workers.cellpose_worker import CellPoseBaseWorker
from cellpose_napari.ressources import getLocalModelsJsonCP3

import numpy as np
from cellpose import io, models

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
        io.logger_setup()
        model = models.CellposeModel(
            gpu=self.use_gpu,
            pretrained_model=self.model_name
        )
        self.model = model

    def run_model(self, im_data, do_3d):
        im_data = self.apply_prefilter(im_data)
        im_data = im_data if do_3d else im_data[:,0,:,:] # CZYX to CYX if 2D
        
        masks, _, _ = self.model.eval(
            im_data,
            diameter=self.diameter,
            anisotropy=self.anisotropy,
            do_3D=do_3d,
            channel_axis=0,
            z_axis=1 if do_3d else None,
            min_size=self.min_object_size,
            flow3D_smooth=self.flow_smooth
        )
        masks = masks if not do_3d else masks[np.newaxis, ...] # YX to ZYX if 2D
        return masks