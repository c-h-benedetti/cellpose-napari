from cellpose_napari.workers.cellpose_training import CellPoseBaseTraining
from cellpose_napari.ressources import (
    getBaseModelsCP3,
    getLocalModelsJsonCP3
)

import json

import numpy as np
from cellpose import (
    io, 
    models, 
    train
)

class CP3TrainingWorker(CellPoseBaseTraining):
    def __init__(self, settings):
        super().__init__(settings)
        self.sgd = settings.get("sgd", False)

    def getCellPoseModels(self):
        base_models = getBaseModelsCP3()
        local_models_json = getLocalModelsJsonCP3()
        local_models = []
        if local_models_json.exists():
            with open(local_models_json, 'r') as f:
                found_models = json.load(f)
                local_models = ["//" + model for model in found_models.keys()]
        return base_models + local_models
    
    def getBaseModelPath(self):
        models_pool = self.getCellPoseModels()
    
    def instanciate_model(self):
        model = models.CellposeModel(
            gpu=self.use_gpu,
            model_type=self.getBaseModelPath()
        )
        data = io.load_train_test_data(
            self.training_folder,
            self.testing_folder,
            mask_filter=self.masks_filter,
            look_one_level_down=self.look_one_level_down
        )
        images, labels, image_names, test_images, test_labels, image_names_test = data
        model_path, train_losses, test_losses = train.train_seg(
            model.net,
            train_data=images,
            train_labels=labels,
            test_data=test_images,
            test_labels=test_labels,
            weight_decay=self.weight_decay,
            learning_rate=self.learning_rate,
            n_epochs=self.n_epochs,
            model_name=self.model_name,
            rescale=self.rescale,
            batch_size=self.batch_size,
            min_train_masks=self.min_train_masks,
            SGD=self.sgd
        )


if __name__ == "__main__":
    settings = {
        'training_folder': "/home/clement/Documents/projects/2219-intensity-membrane/augmented/training",
        'testing_folder': "/home/clement/Documents/projects/2219-intensity-membrane/augmented/testing",
        'look_one_level_down': False,
        'axes': "YX",
        'images_filter': None,
        'masks_filter': "_cp_masks",
        'model_name': "cp-sam-custom-test",
        'base_model': "cpsam",
        'use_gpu': True,
        'weight_decay': 0.1,
        'learning_rate': 0.001,
        'n_epochs': 500,
        'batch_size': 8,
        'rescale': True,
        'min_train_masks': 1,
        'sgd': True
    }
    worker = CP3TrainingWorker(settings)
    worker.run()