from cellpose_napari import (getBaseModels, getLocalModelsJson)
import json


def getCellPoseModels():
    base_models = getBaseModels()
    local_models_json = getLocalModelsJson()
    local_models = []
    if local_models_json.exists():
        with open(local_models_json, 'r') as f:
            found_models = json.load(f)
            local_models = ["//" + model for model in found_models.keys()]
    return base_models + local_models