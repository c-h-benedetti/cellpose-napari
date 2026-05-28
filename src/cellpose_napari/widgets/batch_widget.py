from abc import ABC, abstractmethod

from cellpose_napari.widgets.widget import Widget
from cellpose_napari import CellPoseBatchWorker
from cellpose_napari.widgets.utils import getCellPoseModels

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import napari

from napari.qt.threading import create_worker
from napari.utils.notifications import (
    show_info, 
    show_warning
)
from napari.utils import progress

class BatchWidget(Widget):
    
    def __init__(self, viewer: "napari.viewer.Viewer"): # type: ignore
        super().__init__(viewer)

    def makeBaseOptions(self, options):
        models = getCellPoseModels()
        options.addFolder("Input folder")
        options.addFolder("Output folder")
        options.addStr("Main channel prefix")
        options.addStr("Secondary channel prefix", optional=(True, False))
        options.addChoice("Axes", value="---", choices=["YX", "ZYX", "TYX", "TZYX", "ZTYX"])
        options.addFloat("Pixel size YX", value=1.0)
        options.addFloat("Pixel size Z", value=1.0, optional=(True, False))
        options.addChoice("Model", value=models[0], choices=models)
        options.addInt("Median diameter", value=30)
        options.addInt("Minimum object size", value=15)
        options.addBool("Use GPU?", value=True)
        options.addFloat("Cell probability threshold", value=0.0)
        options.addFloat("Flow threshold", value=0.4)
        options.addFloat("Flow smoothing", value=1.0)
        options.addStr("Segmentation prefix", value="labels-")
    
    def processAnisotropy(self):
        axes = self.options.value("Axes")
        if 'Z' not in axes:
            return 1.0
        pixel_size_z = self.options.value("Pixel size Z")
        pixel_size_yx = self.options.value("Pixel size YX")
        ani = pixel_size_z / pixel_size_yx
        return ani
    
    def apply(self):
        self.operation = None
        try:
            data = self.captureData()
            self.operation = CellPoseBatchWorker(
                data['input_folder'], 
                data['output_folder'], 
                data['main_channel_prefix'], 
                data['secondary_channel_prefix'], 
                data['axes'], 
                data['pixel_size_yx'], 
                data['pixel_size_z'], 
                data['model'], 
                data['median_diameter'], 
                data['min_size'], 
                data['use_gpu'], 
                data['cell_prob_threshold'], 
                data['flow_threshold'], 
                data['flow_smoothing'], 
                data['segmentation_prefix']
            )
        except ValueError as e:
            show_warning(str(e))
            return
        print("batch worker created successfully, starting worker...")
        worker = create_worker(
            self.operation.run,
            _progress={
                'desc': 'Running CellPose batch segmentation...',
                'total': self.operation.get_n_items()
            }
        )
        worker.finished.connect(self.onTaskFinished)
        worker.start()

    def onTaskFinished(self, *args, **kwargs):
        show_info("CellPose batch finished!")

    def captureData(self):
        input_folder = self.options.value("Input folder")
        output_folder = self.options.value("Output folder")
        main_channel_prefix = self.options.value("Main channel prefix")
        secondary_channel_prefix = self.options.value("Secondary channel prefix")
        axes = self.options.value("Axes")
        pixel_size_yx = self.options.value("Pixel size YX")
        pixel_size_z = self.options.value("Pixel size Z") if 'Z' in axes else None
        model = self.options.value("Model")
        median_diameter = self.options.value("Median diameter")
        min_size = self.options.value("Minimum object size")
        use_gpu = self.options.value("Use GPU?")
        cell_prob_threshold = self.options.value("Cell probability threshold")
        flow_threshold = self.options.value("Flow threshold")
        flow_smoothing = self.options.value("Flow smoothing")
        segmentation_prefix = self.options.value("Segmentation prefix")

        return {
            'input_folder': input_folder,
            'output_folder': output_folder,
            'main_channel_prefix': main_channel_prefix,
            'secondary_channel_prefix': secondary_channel_prefix,
            'axes': axes,
            'pixel_size_yx': pixel_size_yx,
            'pixel_size_z': pixel_size_z,
            'model': model,
            'median_diameter': median_diameter,
            'min_size': min_size,
            'use_gpu': use_gpu,
            'cell_prob_threshold': cell_prob_threshold,
            'flow_threshold': flow_threshold,
            'flow_smoothing': flow_smoothing,
            'segmentation_prefix': segmentation_prefix
        }