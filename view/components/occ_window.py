from OCC.Display.backend import load_backend
from PySide2.QtGui import QResizeEvent

from geometry.base_geometry import BaseGeometry
from service.geometry_service import GeometryCollection

load_backend('pyside2')
from OCC.Display import qtDisplay
from PySide2.QtWidgets import QWidget


class OCCWindow(QWidget):

    def __init__(self, parent, geometry_collection: GeometryCollection):
        super().__init__(parent=parent)
        self.canvas = qtDisplay.qtViewer3d(self)
        self.canvas.InitDriver()
        self.canvas.resize(self.width(), self.height())
        self.display = self.canvas._display
        self._geometry_collection = geometry_collection
        self._geometry_collection.on_geometries_change.connect(self.updateView)

    def AddItem(self, source: BaseGeometry):
        self.display.DisplayShape(source.GetShape())

    def updateView(self):
        self.display.EraseAll()
        for geo in self._geometry_collection:
            self.AddItem(geo)
        self.display.FitAll()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.canvas.resize(self.width(), self.height())


