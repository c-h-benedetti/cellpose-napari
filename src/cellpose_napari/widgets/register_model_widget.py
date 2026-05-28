from cellpose_napari.widgets.widget import Widget
import json
from pathlib import Path
from abc import abstractmethod
from napari.utils.notifications import (
    show_info, 
    show_warning
)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import napari


class RegisterModelWidget(Widget):
    
    def __init__(self, viewer: "napari.viewer.Viewer"): # type: ignore
        super().__init__(viewer)

    def makeBaseOptions(self, options):
        options.addStr("Name")
        options.addFile("Model path")
    
    @abstractmethod
    def getLocalModelsJson(self):
        raise NotImplementedError("Subclasses must implement getLocalModelsJson method")

    def apply(self):
        options = self.options
        name = options.value("Name")
        path = options.value("Model path")
        if name is None or path is None:
            show_warning("Name or path is None!")
            return
        path = Path(path)
        if name == "":
            show_warning("Name is empty!")
            return
        if not path.exists() or not path.is_file():
            show_warning("Path does not exist or is not a file!")
            return
        jsonPath = self.getLocalModelsJson()
        data = {}
        if jsonPath.exists():
            with open(jsonPath, "r") as f:
                data = json.load(f)
        data[name] = str(path)
        with open(jsonPath, "w") as f:
            json.dump(data, f, indent=4)
        show_info(f"Model '{name}' registered successfully!")