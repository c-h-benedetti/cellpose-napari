from cellpose_napari.workers.training_cellpose import CellPoseBaseTraining
from cellpose_napari.ressources import (
    getBaseModelsCP3,
    getLocalModelsJsonCP3
)
import json
from cellpose import io, models, train
import xarray as xr


class CP3TrainingWorker(CellPoseBaseTraining):
    
    def __init__(self, settings):
        super().__init__(settings)
        self.sgd = settings.get("use_sgd", False)
        self.default_base = "cyto3"
        io.logger_setup()
    
    def getBaseModelPath(self):
        if self.base_model_name is None:
            return None # Training from scratch.
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
            pretrained_model=base_model
        )

    def formatDataPair(self, images, masks):
        fixed_images = []
        fixed_masks = []
        for img, msk in zip(images, masks):
            if img.shape != msk.shape:
                raise ValueError(f"Image and mask shapes do not match ({img.shape} vs {msk.shape}).")
            if len(img.shape) != len(self.axes):
                raise ValueError(f"Image shape {img.shape} does not match expected number of axes {len(self.axes)}.")
            img = xr.DataArray(img, dims=list(self.axes))
            msk = xr.DataArray(msk, dims=list(self.axes))
            
            if "C" not in img.dims:
                img = img.expand_dims("C")
            img = img.transpose("Y", "X", "C")

            if "C" in msk.dims:
                msk = msk.squeeze("C", drop=True)
            msk = msk.transpose("Y", "X")
            
            fixed_images.append(img.values)
            fixed_masks.append(msk.values)
        return fixed_images, fixed_masks

    def launch_training(self):
        if self.model is None:
            raise Exception("Model not instanciated!")
        
        io.logger_setup()
        print("Loading training data...")
        data = io.load_train_test_data(
            str(self.training_folder),
            str(self.testing_folder),
            mask_filter=self.masks_filter,
            look_one_level_down=self.look_one_level_down
        )
        images, labels, _, test_images, test_labels, _ = data
        images, labels = self.formatDataPair(images, labels)
        if test_images and test_labels:
            test_images, test_labels = self.formatDataPair(test_images, test_labels)
        print(images[0].shape, labels[0].shape)

        print("Starting training...")
        model_path, train_losses, test_losses = train.train_seg(
            self.model.net,
            channels=[1, 0],
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
        self.plot_losses(model_path, train_losses, test_losses)

        self.training_assessment = {
            "model_path"  : model_path,
            "train_losses": train_losses,
            "test_losses" : test_losses
        }
