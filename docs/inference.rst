Inference
=========

* You can drag and drop a variety of images into Napari. 
* You can also open a folder of images to process together (or sequentially). 
* See Napari `image`_ documentation for more advanced image loading.

1. Multi-channel images
-----------------------

Napari is not designed to visualize a composite image (== image with multiple channels) as a single layer.
If you try, you will only be able to visualize one channel at a time, 
without the ability to change the contrast or the colormap of each channel independently.

To handle composites, you can use :code:`cellpose-napari > Split Axis`. 
This will split the composite into multiple layers (one per channel) and add them to the Napari viewer. 
You can then visualize each channel independently and set the settings for each channel independently in the plugin.

The example below shows how to split the channels (cyto and nuclei) and segment the cells using both.

.. raw:: html

   <iframe 
    src="https://www.youtube.com/embed/NT2FDdiqu5A" 
    title="Inference on multi-channel image" 
    frameborder="0" 
    width="800px"
    height="450px"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    allowfullscreen></iframe>

2. Time series
--------------

Time series are handled transparently if you indicate that one of the axes is time.
The result will be a stack with the same shape as the input.

If your time series is actually a set of TIFF files in a folder rather than a stack, 
you can use the "Batch inference" widget to process all the files in the folder together.

.. raw:: html

   <iframe 
    src="https://www.youtube.com/embed/PH_Rd7Z7Dec" 
    title="Inference on time series" 
    frameborder="0" 
    width="800px"
    height="450px"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    allowfullscreen></iframe>

3. Basic workflow for one image
-------------------------------

1. 2D, 2D+t, 2D composites, 2D+t composites, 3D, 3D+t, 3D composites and 3D+t composites images are handled. Start by loading your image in Napari.
2. If it is a composite image, use the "Split Axis" widget to split it into multiple layers (one per channel).
3. If this is a 3D stack, use the "Set calibration" widget to provide the physical size of voxels.
4. Open the "CellPose Inference" widget and select the main channel to segment, and the secondary channel if you have one.
5. Set the axes in the correct order for your image.
6. Set the diameter of the objects to segment. If you change the value, a magenta circle should appear to show you what it looks like on the image.
7. For further details, refer to the `settings`_ page of the documentation.
8. Click "Apply" to launch inference. If you have a time series, the progress bar should be available in the lower left corner of Napari's window.
9. The result will show up as a new 'Labels' layer in the Napari viewer.

.. raw:: html

   <iframe 
    src="https://www.youtube.com/embed/d_nM6wZ4Qjc" 
    title="Inference on single image" 
    frameborder="0" 
    width="800px"
    height="450px"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    allowfullscreen></iframe>


.. _image: https://napari.org/stable/getting_started/open_images.html
.. _settings: settings.html