from OCC.Display.backend import load_backend
from PyQt5.QtGui import QResizeEvent

from geometry.base_geometry import BaseGeometry

load_backend('qt-pyqt5')
from OCC.Display import qtDisplay
from PyQt5.QtWidgets import QWidget


class OCCWindow(QWidget):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.canvas = qtDisplay.qtViewer3d(self)
        self.canvas.InitDriver()
        self.display = self.canvas._display
        self.source_to_shape = {}

    def AddGeometry(self, source: BaseGeometry):
        shape = self.display.DisplayShape(source.GetShape())[0]
        self.source_to_shape.update({source: shape})
        self._UpdateView()

    def RemoveGeometry(self, source: BaseGeometry):
        shape = self.source_to_shape.pop(source)
        self.display.Context.Erase(shape, True)
        self._UpdateView()

    def _UpdateView(self):
        self.display.FitAll()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.canvas.resize(self.width(), self.height())


