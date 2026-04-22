from cellpose_napari import CellPoseBatchWorker

input_folder = "/media/clement/3b801c96-393a-4b2e-be1e-9cabfbb10740/data-formation-ml-dl/dump/PhC-C2DH-U373/01"
output_folder = "/media/clement/3b801c96-393a-4b2e-be1e-9cabfbb10740/data-formation-ml-dl/dump/PhC-C2DH-U373/01_INF"
main_channel_prefix = "t"
secondary_channel_prefix = None
axes = "YX"
pixel_size_yx = 1.0
pixel_size_z = 1.0
model = "cpsam"
median_diameter = 80
min_size = 15
use_gpu = True
cell_prob_threshold = 0.0
flow_threshold = 0.4
flow_smoothing = 0.0
segmentation_prefix = "seg_"

wpbw = CellPoseBatchWorker(
    input_folder, 
    output_folder, 
    main_channel_prefix, 
    secondary_channel_prefix, 
    axes, 
    pixel_size_yx, 
    pixel_size_z, 
    model, 
    median_diameter, 
    min_size, 
    use_gpu, 
    cell_prob_threshold, 
    flow_threshold, 
    flow_smoothing, 
    segmentation_prefix
)

wpbw.run()