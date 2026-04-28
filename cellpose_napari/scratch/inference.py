import tifffile
from pathlib import Path

from cellpose_napari import CellPoseWorker

images_pool = {
    "2D 1C (no time)": {
        'folder'    : Path("/media/clement/3b801c96-393a-4b2e-be1e-9cabfbb10740/data-formation-ml-dl/dump/BBBC022_v1_images_20585w1"),
        'C1'        : "IXMtest_A02_s1_w17C9F8BDB-79F0-4F8B-852B-71161631F236.tif",
        'C2'        : None,
        'diameter'  : 30,
        'anisotropy': 1.0,
        'axes'      : "YX"
    },
    "2D+t 1C": {
        'folder'    : Path("/media/clement/3b801c96-393a-4b2e-be1e-9cabfbb10740/data-formation-ml-dl/dump/PhC-C2DH-U373"),
        'C1'        : "2d+t.tif",
        'C2'        : None,
        'diameter'  : 75,
        'anisotropy': 1.0,
        'axes'      : "TYX"
    },
    "2D 2C (no time)": {
        'folder'    : Path("/media/clement/3b801c96-393a-4b2e-be1e-9cabfbb10740/data-formation-ml-dl/BBBC013-Human-U2OS/tests"),
        'C1'        : "C1--01-A-01.tif",
        'C2'        : "C2--01-A-01.tif",
        'diameter'  : 30,
        'anisotropy': 1.0,
        'axes'      : "YX"
    },
    "2D+t 2C": {
        'folder'    : Path("/media/clement/3b801c96-393a-4b2e-be1e-9cabfbb10740/data-formation-ml-dl/BBBC013-Human-U2OS/tests"),
        'C1'        : "c1_time.tif",
        'C2'        : "c2_time.tif",
        'diameter'  : 30,
        'anisotropy': 1.0,
        'axes'      : "TYX"
    },

    "3D 1C (no time)": {
        'folder'    : Path("/media/clement/3b801c96-393a-4b2e-be1e-9cabfbb10740/Fluo-N3DH-SIM+/01"),
        'C1'        : "t001.tif",
        'C2'        : None,
        'diameter'  : 45,
        'anisotropy': 8.0775,
        'axes'      : "ZYX"
    },
    "3D 2C (no time)": {
        'folder'    : Path("/home/clement/Downloads/2026-03-12-cchamontin/splitted"),
        'C1'        : "C1-CC-VIF-05_24h+BafA_26-1-1.tif",
        'C2'        : "C2-CC-VIF-05_24h+BafA_26-1-1.tif",
        'diameter'  : 180,
        'anisotropy': 3.0894,
        'axes'      : "ZYX"
    },
    "3D+t 1C": {
        'folder'    : Path("/home/clement/Downloads/2026-03-12-cchamontin/splitted"),
        'C1'        : "nuclei-time.tif",
        'C2'        : None,
        'diameter'  : 120,
        'anisotropy': 3.0894,
        'axes'      : "TZYX"
    },
    "3D+t 2C": {
        'folder'    : Path("/home/clement/Downloads/2026-03-12-cchamontin/splitted"),
        'C1'        : "membranes-time.tif",
        'C2'        : "nuclei-time.tif",
        'diameter'  : 240,
        'anisotropy': 3.0894,
        'axes'      : "TZYX"
    }
}

target = "2D 1C (no time)"
folder = images_pool[target]['folder']
c1 = tifffile.imread(folder / images_pool[target]['C1'])
c2 = tifffile.imread(folder / images_pool[target]['C2']) if images_pool[target]['C2'] is not None else None
model = 'cpsam'
diameter = images_pool[target]['diameter']
anisotropy = images_pool[target]['anisotropy']
min_size = 20
cell_prob = 0.0
flow_thr = 0.4
flow_smooth = 0.0
axes = images_pool[target]['axes']

worker = CellPoseWorker(
    ch_main=c1,
    ch_secondary=c2,
    model=model,
    diameter=diameter,
    anisotropy=anisotropy,
    min_size=min_size,
    cell_prob=cell_prob,
    flow_thr=flow_thr,
    flow_smooth=flow_smooth,
    axes=axes,
    use_gpu=True
)

worker.run()
tifffile.imwrite(
    "/tmp/results.tif", 
    worker.output_buffer,
    imagej=True
)