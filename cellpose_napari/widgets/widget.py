from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout
)

from autooptions import OptionsWidget

from abc import abstractmethod

class Widget(QWidget):
    def __init__(self, viewer):
        super().__init__()
        self.viewer     = viewer
        self.sameRowSet = set()
        self.options    = self.getOptions()
        self.widget     = None
        self.operation  = None
        self.createLayout()

    def createLayout(self):
        self.widget = OptionsWidget(
            viewer=self.viewer, 
            options=self.options, 
            layout_type='grid', 
            client=self,
            sameRowSet=self.sameRowSet
        )
        self.widget.addApplyButton(self.apply)
        layout = QVBoxLayout()
        layout.addWidget(self.widget)
        self.setLayout(layout)

    @abstractmethod
    def getOptions(self):
        raise Exception("Abstract method getOptions of class Widget called!")
    
    @abstractmethod
    def apply(self):
        raise Exception("Abstract method apply of class Widget called!")
    