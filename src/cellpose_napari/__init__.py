try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from cellpose_napari.ressources import (
    isCPSAM,
    isCP3
)

from .workers.preprocess import PreprocessingUtils
from .im_utils import ImageUtils

if isCP3():
    from .ressources import getLocalModelsJsonCP3 as getLocalModelsJson
    from .ressources import getBaseModelsCP3 as getBaseModels
    from .workers.inference_cp3 import CP3Inference as CellPoseInference
    from .workers.training_cp3 import CP3TrainingWorker as CellPoseTraining
    from .workers.batch_cpX import CPBatchWorker as CellPoseBatchWorker
    from .widgets.inference_cp3_widget import CP3InferenceWidget as CellPoseInferenceWidget
    from .widgets.training_cp3_widget import CP3TrainingWidget as CellPoseTrainingWidget
    from .widgets.batch_cp3_widget import CP3BatchWidget as CellPoseBatchWidget
    from .widgets.register_model_cp3_widget import CP3RegisterModelWidget as CellPoseRegisterModelWidget
elif isCPSAM():
    from .ressources import getLocalModelsJsonCPSAM as getLocalModelsJson
    from .ressources import getBaseModelsCPSAM as getBaseModels
    from .workers.inference_cpsam import CPSAMInference as CellPoseInference
    from .workers.training_cpsam import CPSAMTrainingWorker as CellPoseTraining
    from .workers.batch_cpX import CPBatchWorker as CellPoseBatchWorker
    from .widgets.inference_cpsam_widget import CPSAMInferenceWidget as CellPoseInferenceWidget
    from .widgets.training_cpsam_widget import CPSAMTrainingWidget as CellPoseTrainingWidget
    from .widgets.batch_cpsam_widget import CPSAMBatchWidget as CellPoseBatchWidget
    from .widgets.register_model_cpsam_widget import CPSAMRegisterModelWidget as CellPoseRegisterModelWidget
else:
    raise Exception(f"Unsupported CellPose version!")

from .widgets.split_axis_widget import SplitAxisWidget
from ._sample_data import napari_provide_sample_data