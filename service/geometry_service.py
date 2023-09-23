from typing import List

from PyQt5.QtCore import pyqtSignal, QObject

from geometry.base_geometry import BaseGeometry
from geometry.geometry_models import Sphere, Cylinder, Cube, Union



class GeometryCollection(QObject):
    on_geometries_change = pyqtSignal()

    def __init__(self):
        super(GeometryCollection, self).__init__()
        self._geometries: List[BaseGeometry] = []

    def createSphere(self, translation=(0.0, 0.0, 0.0), radius=1.0):
        sphere = Sphere(name='Sphere', radius=radius, translation=translation)
        self.appendGeometry(sphere)
        return sphere

    def appendGeometry(self, geometry: BaseGeometry):
        self._geometries.append(geometry)
        self.on_geometries_change.emit()

    def createCylinder(self, translation=(0.0, 0.0, 0.0), radius=1.3, height=1.0):
        cylinder = Cylinder(name='Cylinder', radius=radius, height=height, translation=translation)
        self.appendGeometry(cylinder)
        return cylinder

    def createCube(self, translation=(0.0, 0.0, 0.0)):
        cube = Cube(name='Cube', dx=1.0, dy=1.0, dz=2.0, translation=translation)
        self.appendGeometry(cube)
        return cube

    def unionGeometries(self, translation=(0.0, 0.0, 0.0)):
        # Perform boolean union operation
        union = Union(name='Union', geometries=tuple(self._geometries), translation=translation)
        self.appendGeometry(union)
        return union

    def removeGeometry(self, geometry: BaseGeometry):
        self._geometries.remove(geometry)
        self.on_geometries_change.emit()

    def __iter__(self):
        for geo in self._geometries:
            yield geo

