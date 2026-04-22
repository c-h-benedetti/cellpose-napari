try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from cellpose_napari.ressources import (
    isCPSAM,
    isCP3
)

if isCP3():
    from .workers.cp3_worker import CP3Worker as CellPoseWorker
    from .widgets.cp3_inference_widget import CP3InferenceWidget as CellPoseInferenceWidget
    from .widgets.cp3_training_widget import CP3TrainingWidget as CellPoseTrainingWidget
    from .widgets.cp3_batch_widget import CP3BatchWidget as CellPoseBatchWidget
    from .widgets.cp3_register_model_widget import CP3RegisterModelWidget as CellPoseRegisterModelWidget
elif isCPSAM():
    from .workers.cp_sam_worker import CPSAMWorker as CellPoseWorker
    from .widgets.cpsam_inference_widget import CPSAMInferenceWidget as CellPoseInferenceWidget
    from .widgets.cpsam_training_widget import CPSAMTrainingWidget as CellPoseTrainingWidget
    from .widgets.cpsam_batch_widget import CPSAMBatchWidget as CellPoseBatchWidget
    from .widgets.cpsam_register_model_widget import CPSAMRegisterModelWidget as CellPoseRegisterModelWidget
else:
    raise Exception(f"Unsupported CellPose version!")

from .widgets.split_axis_widget import SplitAxisWidget
from ._sample_data import napari_provide_sample_data
