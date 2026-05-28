import sys
import logging
import json
from platformdirs import user_data_dir
from pathlib import Path
import cellpose

def getCellPoseMajorVersion():
    return int(cellpose.version[0])

def isCPSAM():
    return getCellPoseMajorVersion() == 4

def isCP3():
    return getCellPoseMajorVersion() == 3

def getLocalModelsJsonCP3():
    data_dir = Path(user_data_dir(appname="cellpose_napari", appauthor="mri_cia"))
    if not data_dir.exists():
        print("Creating data directory for local models:", data_dir)
        data_dir.mkdir(parents=True, exist_ok=True)
    json_path = data_dir / "local_models_cp3.json"
    if not json_path.exists():
        print("Creating local models JSON file:", json_path)
        with open(json_path, 'w') as f:
            json.dump({}, f)
    print("Local models JSON location:", json_path)
    return json_path

def getLocalModelsJsonCPSAM():
    data_dir = Path(user_data_dir(appname="cellpose_napari", appauthor="mri_cia"))
    if not data_dir.exists():
        print("Creating data directory for local models:", data_dir)
        data_dir.mkdir(parents=True, exist_ok=True)
    json_path = data_dir / "local_models_cpsam.json"
    if not json_path.exists():
        print("Creating local models JSON file:", json_path)
        with open(json_path, 'w') as f:
            json.dump({}, f)
    print("Local models JSON location:", json_path)
    return json_path

def getBaseModelsCP3():
    return [
        "cyto3", 
        "cyto2", 
        "cyto", 
        "nuclei",
        "tissuenet_cp3", 
        "livecell_cp3", 
        "yeast_PhC_cp3", 
        "yeast_BF_cp3", 
        "bact_phase_cp3", 
        "bact_fluor_cp3",
        "deepbacs_cp3",
        "cyto2_cp3"
    ]

def getBaseModelsCPSAM():
    return [
        "cpsam"
    ]

def init_logger():
    logger = logging.getLogger(__name__)
    if '--verbose' in sys.argv or '-v' in sys.argv:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
    return logger