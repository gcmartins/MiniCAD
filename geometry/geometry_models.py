from typing import Tuple

from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeBox
from attr import Factory
from attrs import define

from geometry.base_geometry import BaseGeometry


@define
class Sphere(BaseGeometry):
    radius: float = 1

    def Draw(self):
        shape = BRepPrimAPI_MakeSphere(self.radius).Shape()
        return shape


@define
class Cylinder(BaseGeometry):
    radius: float = 1.0
    height: float = 1.0

    def Draw(self):
        shape = BRepPrimAPI_MakeCylinder(self.radius, self.height).Shape()
        return shape


@define
class Cube(BaseGeometry):
    dx: float = 1.0
    dy: float = 1.0
    dz: float = 1.0

    def Draw(self):
        shape = BRepPrimAPI_MakeBox(self.dx, self.dy, self.dz).Shape()
        return shape


@define
class Union(BaseGeometry):
    geometries: Tuple[BaseGeometry] = Factory(Tuple[BaseGeometry])

    def Draw(self):
        shapes = [geo.GetShape() for geo in self.geometries]
        union = BRepAlgoAPI_Fuse(*shapes)
        return union.Shape()
