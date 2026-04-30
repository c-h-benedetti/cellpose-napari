from cellpose_napari.workers.cellpose_training import CellPoseBaseTraining
from cellpose_napari.ressources import (
    getBaseModelsCP3,
    getLocalModelsJsonCP3
)
import json
from cellpose import io, models, train


class CP3TrainingWorker(CellPoseBaseTraining):
    
    def __init__(self, settings):
        super().__init__(settings)
        self.sgd = settings.get("use_sgd", False)
        self.default_base = "cyto3"
    
    def getBaseModelPath(self):
        if not self.base_model_name.startswith("//"):
            if self.base_model_name not in getBaseModelsCP3():
                print(f"Model not found, going with '{self.default_base}' base model.")
                return self.default_base
            return self.base_model_name
        json_path = getLocalModelsJsonCP3()
        if not json_path.exists():
            raise ValueError(f"Local models json file '{json_path}' does not exist.")
        with open(json_path, 'r') as f:
            found_models = json.load(f)
            model_name = self.base_model_name[2:]
            if model_name not in found_models:
                print(f"Model not found, going with '{self.default_base}' base model.")
                return self.default_base
            return found_models[model_name]
    
    def instanciate_model(self):
        base_model = self.getBaseModelPath()
        print(f"Using base model: {base_model}")
        self.model = models.CellposeModel(
            gpu=self.use_gpu,
            model_type=base_model
        )

    def launch_training(self):
        if self.model is None:
            raise Exception("Model not instanciated!")
        
        print("Loading training data...")
        data = io.load_train_test_data(
            str(self.training_folder),
            str(self.testing_folder),
            mask_filter=self.masks_filter,
            look_one_level_down=self.look_one_level_down
        )
        images, labels, _, test_images, test_labels, _ = data

        print("Starting training...")
        model_path, train_losses, test_losses = train.train_seg(
            self.model.net,
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
            min_train_masks=self.min_train_masks
        )

        self.training_assessment = {
            "model_path"  : model_path,
            "train_losses": train_losses,
            "test_losses" : test_losses
        }
