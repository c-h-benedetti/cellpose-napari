from cellpose_napari.widgets.widget import Widget

import json
from pathlib import Path

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import napari

from abc import abstractmethod

class RegisterModelWidget(Widget):
    
    def __init__(self, viewer: "napari.viewer.Viewer"):
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
            print("Name or path is None!")
            return
        path = Path(path)
        if name == "":
            print("Name is empty!")
            return
        if not path.exists() or not path.is_file():
            print("Path does not exist or is not a file!")
            return
        jsonPath = self.getLocalModelsJson()
        data = {}
        if jsonPath.exists():
            with open(jsonPath, "r") as f:
                data = json.load(f)
        data[name] = str(path)
        with open(jsonPath, "w") as f:
            json.dump(data, f, indent=4)