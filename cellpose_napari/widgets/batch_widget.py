from qtpy.QtWidgets import (
    QVBoxLayout
)

from cellpose_napari.widgets.widget import Widget

from autooptions import Options
from autooptions import OptionsWidget

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import napari

class BatchWidget(Widget):
    
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__(viewer)

    def makeBaseOptions(self, options):
        pass
