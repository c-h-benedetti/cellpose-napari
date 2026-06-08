Installation
============

It is recommended to install this plugin in a new Python environment, to avoid collisions.
Choose a tool among conda/miniconda, pipenv, poetry, venv, ... to create a new environment and install the plugin in it.
The following "quick way" instructions assume that you are in an active environment and have pip installed.

1. Install Napari (if not already done)
---------------------------------------

* For full Napari install instructions, look at their `install`_ instructions.
* Otherwise, a quick way to do it is to use :code:`pip install napari[all]`.

2. Install Cellpose (if not already done)
-----------------------------------------

* For full Cellpose install instructions, look up the main Cellpose github `readme`_. 
* This plugin is compatible with both Cellpose 3 and Cellpose 4 (Cellpose SAM), so you can install either version.
* Otherwise, the quick way to proceed is as follows.

A. Install PyTorch
~~~~~~~~~~~~~~~~~~

* If you have an NVidia GPU, you can install a version of PyTorch embedding CUDA drivers by following the instructions on the `PyTorch website`_.
* Otherwise, you can install the CPU version of PyTorch with the following command: :code:`pip install torch`.

B. Install Cellpose itself
~~~~~~~~~~~~~~~~~~~~~~~~~~

* If you would like to go with Cellpose 3, you can run the command :code:`pip install cellpose==3.1.1`.
* If you would like to go with Cellpose 4 (Cellpose SAM), you can run the command :code:`pip install "cellpose>=4"`.

3. Install Cellpose-Napari
--------------------------

* To install Cellpose-Napari, you can run the command :code:`pip install cellpose-napari`.
* You can also install the latest development version of Cellpose-Napari with the command :code:`pip install git+https://github.com/MouseLand/cellpose-napari.git`. This latest way requires git to be installed on your system.

4. Common issues
----------------

If you receive the error: ``Illegal instruction (core dumped)``, then
likely mxnet does not recognize your MKL version. Please uninstall and
reinstall mxnet without mkl:

::

   pip uninstall mxnet-mkl
   pip uninstall mxnet
   pip install mxnet==1.4.0

If you receive the error: ``No module named PyQt5.sip``, then try
uninstalling and reinstalling pyqt5

::

   pip uninstall pyqt5 pyqt5-tools
   pip install pyqt5 pyqt5-tools pyqt5.sip

If you have errors related to OpenMP and libiomp5, then try 

::
   conda install nomkl

If you receive an error associated with **matplotlib**, try upgrading
it:

::

   pip install matplotlib --upgrade

If you receive the error: ``ImportError: _arpack DLL load failed``, then try uninstalling and reinstalling scipy
::

   pip uninstall scipy
   pip install scipy

If you are having issues with the graphical interface, make sure you have **python 3.7** and not python 3.8 installed.

If you are on Yosemite Mac OS or earlier, PyQt doesn't work and you won't be able
to use the graphical interface for cellpose. More recent versions of Mac
OS are fine. The software has been heavily tested on Windows 10 and
Ubuntu 18.04, and less well tested on Mac OS. Please post an issue if
you have installation problems.

.. _readme: http://github.com/mouseland/cellpose
.. _install: https://napari.org/tutorials/fundamentals/installation.html
.. _PyTorch website: https://pytorch.org/get-started/locally/