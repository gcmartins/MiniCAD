from PySide2.QtCore import QObject, Signal

from geometry.base_geometry import BaseGeometry


class SelectionService(QObject):
    on_selection_changed = Signal(BaseGeometry)

    item_selected: BaseGeometry

    def __init__(self):
        super().__init__()

    def SetSelected(self, geometry: BaseGeometry):
        self.item_selected = geometry
        self.on_selection_changed.emit(geometry)
