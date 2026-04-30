from cellpose_napari import CellPoseTraining

settings = {
    'training_folder'    : "/home/clement/Documents/projects/2219-intensity-membrane/augmented/training",
    'testing_folder'     : "/home/clement/Documents/projects/2219-intensity-membrane/augmented/testing",
    'look_one_level_down': False,
    'axes'               : "YX",
    'images_filter'      : None,
    'masks_filter'       : "_cp_masks",
    'model_name'         : "cp-sam-custom-test",
    'base_model'         : "cpsam",
    'use_gpu'            : True,
    'weight_decay'       : 0.1,
    'learning_rate'      : 0.001,
    'n_epochs'           : 500,
    'batch_size'         : 8,
    'rescale'            : True,
    'min_train_masks'    : 1,
    'sgd'                : True
}

worker = CellPoseTraining(settings)
worker.run()