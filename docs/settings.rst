Settings
========

* There are more settings for Cellpose that can be accessed using the CLI or 
through a Jupyter notebook. See details at cellpose `docs`_.
* Listed are settings available through the Napari widget.
* Please file an issue if you would like a new setting available in the widget.

Main & secondary channels
-------------------------

* The main channel is the channel containing your objects of interest.
* The secondary channel is an **optional** channel that can be used to help segmentation.
  For example, you can provide a nuclear channel as the secondary channel when segmenting the cytoplasm.
* If you are using Cellpose SAM, there should not be any effect if you swap the main and secondary channels.
* Both these channels should be independent layers in Napari.

Axes
----

* An image with three dimensions could be a 3D image (Z, Y, X) or a time series (T, Y, X).
* Also, according to the source, an image with four dimensions could have the shape (T, Z, Y, X) or (Z, T, Y, X).
* Due to this variability and the multiple ways this information can be encoded in the metadata, 
  the plugin does not try to guess the axes order and instead asks the user to set it.

Model
-----

* Cellpose SAM comes with a single pretrained model called "cpsam".
* Cellpose 3 comes with many more models such as "cyto3", "nuclei" or "tissuenet_cp3".
  You can go to Cellpose documentation to find a more detailed list of these `models`_.
* If you launch the "Register CellPose Model" widget, 
  you will be able to provide a name and a path for a custom model.
* Your custom models will appear with the "//" prefix in the model dropdown menu.

Median diameter
---------------

* The Cellpose models have been trained on images that were rescaled 
  to all have the same diameter (30 pixels in the case of the `cyto` 
  model and 17 pixels in the case of the `nuclei` model). Therefore, 
  Cellpose needs a user-defined cell diameter (in pixels) as input, or to estimate 
  the object size on an image-by-image basis.
* Changing the diameter will change the results that the algorithm 
  outputs. When the diameter is set smaller than the true size 
  then cellpose may over-split cells. Similarly, if the diameter 
  is set too big then cellpose may over-merge cells.
* If you edit the diameter value, a magenta circle will appear.
  You can translate it as you need, and it should show up on the current slice.

Minimum object size
-------------------

* The minimum object size is the minimum number of pixels that a label needs to have to be kept in the final result.
* You can adjust it to remove small objects or debris from the final segmentation.

Use GPU?
--------

* This checkbox allows you to choose whether to run Cellpose on the GPU or on the CPU.
* Only NVidia GPUs are supported and PyTorch requires CUDA drivers to run on the GPU.

Cell probability threshold
--------------------------

The network predicts 3 outputs:

* Flows in X
* Flows in Y
* Cells "probability"

* The probabilities prediction are the inputs to a sigmoid centered at zero (1 / (1 + e^-x)), 
so they vary from around -6 to +6. The pixels greater than the 
``cellprob_threshold`` are used to run dynamics and determine masks. 
* The default is ``cellprob_threshold=0.0``. 
* Decrease this threshold if Cellpose is not returning  as many masks as you'd expect. 
* Increase it if Cellpose is returning too masks particularly from dim areas.

Flow threshold
--------------

Placeholder

Flow smoothing
--------------

Placeholder

Segmentation prefix
-------------------

Placeholder


















Resample
~~~~~~~~~~~~~~~~~~~~~~~~

The cellpose network is run on your rescaled image -- where the rescaling factor is determined 
by the diameter you input (or determined automatically as above). For instance, if you have 
an image with 60 pixel diameter cells, the rescaling factor is 30./60. = 0.5. After determining 
the flows (dX, dY, cellprob), the model runs the dynamics. The dynamics can be run at the rescaled 
size (``resample=False``), or the dynamics can be run on the resampled, interpolated flows 
at the true image size (``resample=True``). ``resample=True`` will create smoother masks when the 
cells are large but will be slower in case; ``resample=False`` will find more masks when the cells 
are small but will be slower in this case.


.. _docs: https://cellpose.readthedocs.io/en/latest/command.html#command-line
.. _models: https://cellpose.readthedocs.io/en/v3.1.1.1/models.html




