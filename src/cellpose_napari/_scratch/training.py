from cellpose_napari import CellPoseTraining

settings = {
    'training_folder'    : "/home/clement/Desktop/cellpose_napari_wd/training_datasets/training",
    'testing_folder'     : "/home/clement/Desktop/cellpose_napari_wd/training_datasets/testing",
    'look_one_level_down': False,
    'axes'               : "YXC",
    'images_filter'      : None,
    'masks_filter'       : "_cp_masks",
    'model_name'         : "yeasts",
    'base_model'         : 'cyto3',
    'use_gpu'            : True,
    'weight_decay'       : 0.1,
    'learning_rate'      : 0.001,
    'n_epochs'           : 250,
    'batch_size'         : 8,
    'rescale'            : True,
    'min_train_masks'    : 1,
    'sgd'                : False
}

worker = CellPoseTraining(settings)
worker.run()