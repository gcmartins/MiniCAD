from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from attrs import asdict

from geometry.base_geometry import BaseGeometry


class TreeWidget(QTreeWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setIndentation(10)
        self.setColumnCount(2)
        self.setHeaderLabels(["Name", "Value"])

        self._items = {}

    def AddGeometryItem(self, geometry: BaseGeometry):
        item = QTreeWidgetItem(self, [geometry.name])

        attributes = asdict(geometry)

        for key, value in attributes.items():
            radius_item = QTreeWidgetItem(item, [key, str(value)])
            item.addChild(radius_item)

        self.addTopLevelItem(item)

        self._items.update({geometry: item})

    def RemoveGeometryItem(self, geometry: BaseGeometry):
        item = self._items.pop(geometry)
        for i in item.takeChildren():
            item.removeChild(i)

        top_item = self.takeTopLevelItem(0)
        del top_item







