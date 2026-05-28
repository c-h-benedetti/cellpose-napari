import numpy as np
import xarray as xr
from abc import abstractmethod
from cellpose_napari.widgets.widget import Widget
from cellpose_napari import (
    CellPoseInference, 
    ImageUtils
)
from cellpose_napari.widgets.utils import getCellPoseModels
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import napari
from napari.qt.threading import create_worker
from napari.utils.notifications import show_info, show_warning


class InferenceWidget(Widget):

    def __init__(self, viewer: "napari.viewer.Viewer"):  # type: ignore
        super().__init__(viewer)

    def makeBaseOptions(self, options):
        models = getCellPoseModels()
        options.addImage("Main channel")
        options.addImage("Secondary channel", optional=[True, False])
        options.addChoice(
            "Axes", value="---", choices=["YX", "ZYX", "TYX", "TZYX", "ZTYX"]
        )
        options.addChoice("Model", value=models[0], choices=models, transient=True)
        options.addInt(
            "Median diameter", value=30, callback=self.updateMedianDiameterCallback
        )
        options.addInt("Minimum object size", value=15)
        options.addBool("Use GPU?", value=True)
        options.addFloat("Cell probability threshold", value=0.0)
        options.addFloat("Flow threshold", value=0.4)
        options.addFloat("Flow smoothing", value=1.0)
        options.addStr("Segmentation prefix", value="cp-labels-")

    def updateMedianDiameterCallback(self):
        if self.widget is None:
            return
        self.widget._transferValues()
        layer = self.widget.getImageLayer("Main channel")
        if layer is None:
            return
        w = self.options.value("Median diameter")
        n = "Median diameter preview"
        s = layer.data.shape
        pt = layer._data_slice.point
        if any([np.isnan(pt[i]) for i in range(len(s) - 2)]):
            show_warning("Please switch to the 2D view for the diameter preview to work.")
            return
        pad = [int(pt[i]) for i in range(len(s) - 2)]
        upper_left = np.array([s[-2] - w, 0])  # lower left corner
        corners = np.array(
            [  # corners of the circle's bounding box
                (*pad, 0, 0),
                (*pad, 0, w),
                (*pad, w, w),
                (*pad, w, 0),
            ]
        )

        if n in self.viewer.layers:
            circle = self.viewer.layers[n].data[0]
            center = np.mean(circle, axis=0)
            upper_left = center - np.array([*pad, w / 2, w / 2])
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
                scale=layer.scale,
                translate=layer.translate,
                metadata=layer.metadata,
                units=layer.units
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
        if "Z" not in vals:
            return 1.0
        return vals["Z"] / vals["Y"]

    def captureData(self):
        axes = self.options.value("Axes")
        anisotropy = self.processAnisotropy()
        model = self.options.value("Model")
        diameter = self.options.value("Median diameter")
        min_size = self.options.value("Minimum object size")
        cell_prob = self.options.value("Cell probability threshold")
        flow_thr = self.options.value("Flow threshold")
        flow_smooth = self.options.value("Flow smoothing")
        use_gpu = self.options.value("Use GPU?")

        main_channel_layer = self.widget.getImageLayer("Main channel")
        if main_channel_layer is None:
            raise ValueError("Main channel layer is required")
        main_channel = xr.DataArray(main_channel_layer.data, dims=list(axes))
        main_channel = ImageUtils.ensureAxes(main_channel)

        secondary_channel_name = self.options.value("Secondary channel")
        if secondary_channel_name is None:
            secondary_channel_layer = None
        else:
            secondary_channel_layer = self.viewer.layers[secondary_channel_name]

        secondary_channel = (
            xr.DataArray(secondary_channel_layer.data, dims=list(axes))
            if secondary_channel_layer
            else None
        )
        secondary_channel = (
            ImageUtils.ensureAxes(secondary_channel) 
            if secondary_channel is not None 
            else None
        )
        
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
            self.operation = CellPoseInference(
                data["main_channel"],
                data["secondary_channel"],
                data["model"],
                data["diameter"],
                data["anisotropy"],
                data["min_size"],
                data["cell_prob"],
                data["flow_thr"],
                data["flow_smooth"],
                data["use_gpu"],
            )
        except ValueError as e:
            show_warning(str(e))
            return
        
        print("worker created successfully, starting worker...")
        worker = create_worker(
            self.operation.run,
            _progress={
                "desc": "Running CellPose segmentation...",
                "total": self.operation.get_n_time_points(),
            },
        )
        
        worker.finished.connect(self.displayResult)
        worker.start()

    def displayResult(self, *args, **kwargs):
        print("Worker finished, displaying results...")
        if self.operation is None:
            show_info("No output to display")
            return
        if self.operation.output_buffer is None:
            show_info("No output to display")
            return
        prefix = self.options.value("Segmentation prefix")
        layer = self.widget.getImageLayer("Main channel")
        if layer is None:
            show_info("Main channel layer not found, cannot display results")
            return
        name = prefix + layer.name
        axes = self.options.value("Axes")
        result = ImageUtils.removeExtraAxes(self.operation.output_buffer, axes)
        if name in self.viewer.layers:
            self.viewer.layers[name].data = result.values
        else:
            self.viewer.add_labels(
                result.values,
                name=name,
                scale=layer.scale,
                translate=layer.translate,
                metadata=layer.metadata,
                units=layer.units
            )
