from cellpose_napari.workers.inference_cellpose import CellPoseBaseInference
from cellpose_napari.ressources import getLocalModelsJsonCPSAM
import xarray as xr
from cellpose_napari import ImageUtils
from cellpose import io, models


class CPSAMInference(CellPoseBaseInference):
    def __init__(
            self, 
            ch_main, 
            ch_secondary, 
            model='cpsam', 
            diameter=30, 
            anisotropy=1.0, 
            min_size=15, 
            cell_prob=0.0, 
            flow_thr=0.4, 
            flow_smooth=0, 
            use_gpu=True,
            kill_border=False,
            margin_width=1
        ):
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
            use_gpu,
            kill_border,
            margin_width
        )

    def get_json_models_path(self):
        return getLocalModelsJsonCPSAM()
    
    def instanciate_model(self):
        io.logger_setup()
        model = models.CellposeModel(
            gpu=self.use_gpu,
            pretrained_model=self.model_name
        )
        return model

    def run_model(self, im_data, do_3d, model):
        r = -1
        if not do_3d:
            im_data, r = ImageUtils.removeAxis(im_data, "Z")
        else:
            r = im_data.dims.index("Z")
        
        c_idx = im_data.dims.index("C")
        masks, _, _ = model.eval(
            im_data.values,
            diameter=self.diameter,
            anisotropy=self.anisotropy,
            do_3D=do_3d,
            channel_axis=c_idx,
            z_axis=r if do_3d else None,
            min_size=self.min_object_size,
            flow3D_smooth=self.flow_smooth
        )

        masks = self.killBorder(masks)
        masks = xr.DataArray(masks, dims=[a for a in im_data.dims if a != "C"])
        masks = ImageUtils.ensureAxes(masks, [str(a) for a in im_data.dims])
        return masks
