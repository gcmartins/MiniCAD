from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QPushButton
from attrs import asdict

from geometry.base_geometry import BaseGeometry
from service.geometry_service import GeometryCollection


class GeometryTreeWidget(QTreeWidget):

    def __init__(self, parent, geometry_collection: GeometryCollection):
        super().__init__(parent)
        self.setIndentation(10)
        self.setColumnCount(3)
        self.setHeaderLabels(["Name", "Value", "Actions"])
        self._geometry_collection = geometry_collection
        self._geometry_collection.on_geometries_change.connect(self.updateItems)

    def AddItem(self, geometry: BaseGeometry):
        item = QTreeWidgetItem(self, [geometry.name])

        attributes = asdict(geometry)

        for key, value in attributes.items():
            geo_item = QTreeWidgetItem(item, [key, str(value)])
            item.addChild(geo_item)

        self.addTopLevelItem(item)

        button = QPushButton('Delete')
        button.clicked.connect(lambda: self._geometry_collection.removeGeometry(geometry))
        self.setItemWidget(item, 2, button)

    def updateItems(self):
        self.clear()
        for geo in self._geometry_collection:
            self.AddItem(geo)







