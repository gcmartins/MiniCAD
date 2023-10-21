from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QPushButton

from geometry.base_geometry import BaseGeometry
from service.geometry_service import GeometryCollection
from service.selection_service import SelectionService


class GeometryTreeWidget(QTreeWidget):

    def __init__(self, parent, geometry_collection: GeometryCollection, selection_service: SelectionService):
        super().__init__(parent)
        self.setIndentation(10)
        self.setColumnCount(3)
        self.setHeaderLabels(["Name", "Value", "Actions"])
        self._geometry_collection = geometry_collection
        self._geometry_collection.on_geometries_change.connect(self.updateItems)
        self._selection_service = selection_service
        self.itemClicked.connect(self.SelectionChanged)
        self._item_to_geometry = {}

    def SelectionChanged(self, item, column):
        self._selection_service.SetSelected(self._item_to_geometry[item])

    def AddItem(self, geometry: BaseGeometry):
        item = QTreeWidgetItem(self, [geometry.name])

        attributes = geometry.__dict__

        for key, value in attributes.items():
            geo_item = QTreeWidgetItem(item, [key, str(value)])
            item.addChild(geo_item)

        self.addTopLevelItem(item)

        button = QPushButton('Delete')
        button.clicked.connect(lambda: self._geometry_collection.removeGeometry(geometry))
        self.setItemWidget(item, 2, button)
        self._item_to_geometry[item] = geometry

    def updateItems(self):
        self.clear()
        for geo in self._geometry_collection:
            self.AddItem(geo)
