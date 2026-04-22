from qtpy.QtWidgets import (
    QVBoxLayout
)

from autooptions.qtutil import WidgetTool
from cellpose_napari.widgets.widget import Widget
from cellpose_napari import CellPoseWorker

import numpy as np

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import napari

from napari.qt.threading import create_worker
from napari.utils.notifications import (
    show_info, 
    show_warning
)

from abc import abstractmethod

class InferenceWidget(Widget):
    
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__(viewer)
        self.updateAxesCallback()

    def makeBaseOptions(self, options):
        models = self.getCellPoseModels()
        options.addImage("Main channel", callback=self.updateAxesCallback)
        options.addImage("Secondary channel", optional=(True, False))
        options.addChoice("Axes", value="---", choices=["---"])
        options.addChoice("Model", value=models[0], choices=models)
        options.addInt("Median diameter", value=30, callback=self.updateMedianDiameterCallback)
        options.addInt("Minimum object size", value=15)
        options.addBool("Use GPU?", value=True)
        options.addFloat("Cell probability threshold", value=0.0)
        options.addFloat("Flow threshold", value=0.4)
        options.addFloat("Flow smoothing", value=1.0)
        options.addStr("Segmentation suffix", value="_cp_masks")

    @abstractmethod
    def getCellPoseModels(self):
        raise Exception("Abstract method getCellPoseModels of class InferenceWidget called!")

    def updateAxesCallback(self):
        self.widget._transferValues()
        layer = self.widget.getImageLayer("Main channel")
        w = self.widget.widgets['Axes']
        pool = ["YX", "ZYX", "TYX", "TZYX", "ZTYX"]
        new_items = ["---"] if layer is None else [p for p in pool if len(p) == len(layer.data.shape)]
        WidgetTool.replaceItemsInComboBox(w, new_items)

    def updateMedianDiameterCallback(self):
        self.widget._transferValues()
        layer = self.widget.getImageLayer("Main channel")
        if layer is None:
            return
        w = self.options.value("Median diameter")
        n = "Median diameter preview"
        s = layer.data.shape
        pt = layer._data_slice.point
        pad = [int(pt[i]) for i in range(len(s) - 2)]
        upper_left = np.array([ # lower left corner
            s[-2] - w,
            0
        ])
        corners = np.array([ # corners of the circle's bounding box
            (*pad, 0, 0),
            (*pad, 0, w),
            (*pad, w, w),
            (*pad, w, 0),
        ])

        if n in self.viewer.layers:
            circle = self.viewer.layers[n].data[0]
            center = np.mean(circle, axis=0)
            upper_left = center - np.array([*pad, w/2, w/2])
            for i in range(len(pad)):
                upper_left[i] = 0
            corners = corners + upper_left
            self.viewer.layers[n].data = corners
        else:
            corners = corners + np.array([0 for _ in range(len(pad))] + [*upper_left])
            self.viewer.add_shapes(
                corners, 
                shape_type="ellipse", 
                edge_color="magenta", 
                face_color="magenta",
                name=n,
                scale=layer.scale
            )

    def processAnisotropy(self):
        layer = self.widget.getImageLayer("Main channel")
        axes = self.options.value("Axes")
        if layer is None:
            return 1.0
        calib = layer.scale
        vals = {}
        for v, a in zip(axes, calib):
            vals[a] = v
        if 'Z' not in vals:
            return 1.0
        return vals['Z'] / vals['Y']

    def captureData(self):
        main_channel_layer = self.widget.getImageLayer("Main channel")
        if main_channel_layer is None:
            raise ValueError("Main channel layer is required")
        main_channel = main_channel_layer.data

        use_secondary = self.options.isActive("Secondary channel")
        secondary_channel_layer = self.widget.getImageLayer("Secondary channel")
        if use_secondary and secondary_channel_layer is None:
            raise ValueError("Secondary channel layer is active but not found")
        secondary_channel = secondary_channel_layer.data if use_secondary else None

        anisotropy = self.processAnisotropy()

        model = self.options.value("Model")

        diameter = self.options.value("Median diameter")

        min_size = self.options.value("Minimum object size")

        cell_prob = self.options.value("Cell probability threshold")

        flow_thr = self.options.value("Flow threshold")

        flow_smooth = self.options.value("Flow smoothing")

        axes = self.options.value("Axes")

        use_gpu = self.options.value("Use GPU?")

        return {
            "main_channel": main_channel,
            "secondary_channel": secondary_channel,
            "model": model,
            "diameter": diameter,
            "anisotropy": anisotropy,
            "min_size": min_size,
            "cell_prob": cell_prob,
            "flow_thr": flow_thr,
            "flow_smooth": flow_smooth,
            "axes": axes,
            "use_gpu": use_gpu
        }

    def apply(self):
        self.operation = None
        try:
            data = self.captureData()
            self.operation = CellPoseWorker(
                data["main_channel"],
                data["secondary_channel"],
                data["model"],
                data["diameter"],
                data["anisotropy"],
                data["min_size"],
                data["cell_prob"],
                data["flow_thr"],
                data["flow_smooth"],
                data["axes"],
                data["use_gpu"]
            )
        except ValueError as e:
            show_warning(str(e))
            return
        print("worker created successfully, starting worker...")
        worker = create_worker(
            self.operation.run,
            _progress={'desc': 'Running CellPose segmentation...'}
        )
        worker.finished.connect(self.displayResult)
        worker.start()

    def displayResult(self):
        print("Worker finished, displaying results...")
        if self.operation.output_buffer is None:
            show_info("No output to display")
            return
        suffix = self.options.value("Segmentation suffix")
        layer = self.widget.getImageLayer("Main channel")
        name = layer.name + suffix
        if name in self.viewer.layers:
            self.viewer.layers[name].data = self.operation.output_buffer
        else:
            self.viewer.add_labels(
                self.operation.output_buffer, 
                name=name,
                scale=layer.scale,
                translate=layer.translate
            )