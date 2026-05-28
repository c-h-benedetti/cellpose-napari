from cellpose_napari.widgets.widget import Widget

from autooptions import Options

import numpy as np

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import napari
from napari.utils.notifications import (
    show_warning,
    show_info
)

class SplitAxisWidget(Widget):
    
    def __init__(self, viewer: "napari.viewer.Viewer"): # type: ignore
        super().__init__(viewer)
        self.base_luts = ["red", "green", "blue", "cyan", "magenta", "yellow"]
        self.showShapeCallback()

    def getOptions(self):
        options = Options("NapariCellpose", "Split Axis")
        options.addImage("Target image", callback=self.showShapeCallback)
        options.addInt("Axis to split", value=0)
        options.addStr("LUTs", value="red, green, blue, cyan, magenta, yellow", optional=(True, False))
        options.addBool("Delete original?", value=True)
        options.load()
        return options
    
    def showShapeCallback(self):
        self.widget._transferValues()
        layer = self.widget.getImageLayer("Target image")
        if layer is not None:
            show_info(' | '.join([f'Axis {i}: {s}' for i, s in enumerate(layer.data.shape)]))
    
    def updateLUTs(self):
        luts = self.options.value("LUTs")
        if luts is None or luts.strip() == "":
            return
        self.base_luts = [lut.strip() for lut in luts.lower().split(",")]
    
    def apply(self):
        layer = self.widget.getImageLayer("Target image")
        if layer is None:
            return
        axis = self.options.value("Axis to split")
        if axis < 0 or axis >= len(layer.data.shape):
            show_warning(f"Invalid axis {axis} for image with shape {layer.data.shape}")
            return
        self.updateLUTs()
        delete_original = self.options.value("Delete original?")
        for i in range(layer.data.shape[axis]):
            data = layer.data.take(i, axis=axis)
            scale = tuple(s for j, s in enumerate(layer.scale) if j != axis) if layer.scale is not None else None
            translate = tuple(s for j, s in enumerate(layer.translate) if j != axis) if layer.translate is not None else None
            self.viewer.add_image(
                data, 
                name=f"#{i+1} - {layer.name}",
                scale=scale,
                translate=translate,
                opacity=layer.opacity,
                blending=layer.blending,
                visible=layer.visible,
                metadata=layer.metadata,
                colormap=self.base_luts[i % len(self.base_luts)] if self.base_luts else None
            )
        if delete_original:
            self.viewer.layers.remove(layer)