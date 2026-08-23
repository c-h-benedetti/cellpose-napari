from abc import abstractmethod
from autooptions import OptionsWidget
from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout
)

class Widget(QWidget):
    def __init__(self, viewer):
        super().__init__()
        self.viewer     = viewer
        self.sameRowSet = set()
        self.options    = self.getOptions()
        self.operation  = None
        self.widget     = self.createLayout()

    def setEnabledGUI(self, enabled: bool):
        self.widget.setEnabled(enabled)

    def createLayout(self):
        widget = OptionsWidget(
            viewer=self.viewer, 
            options=self.options, 
            layout_type='grid', 
            client=self,
            sameRowSet=self.sameRowSet
        )
        widget.addApplyButton(self.apply)
        layout = QVBoxLayout()
        layout.addWidget(widget)
        self.setLayout(layout)
        return widget

    @abstractmethod
    def getOptions(self):
        raise Exception("Abstract method getOptions of class Widget called!")
    
    @abstractmethod
    def apply(self):
        raise Exception("Abstract method apply of class Widget called!")
    