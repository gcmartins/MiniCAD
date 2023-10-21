from typing import Tuple

from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeBox

from geometry.base_geometry import BaseGeometry


class Sphere(BaseGeometry):
    radius: float = 1.0

    def Draw(self):
        shape = BRepPrimAPI_MakeSphere(self.radius).Shape()
        return shape


class Cylinder(BaseGeometry):
    radius: float = 1.0
    height: float = 1.0

    def Draw(self):
        shape = BRepPrimAPI_MakeCylinder(self.radius, self.height).Shape()
        return shape


class Cube(BaseGeometry):
    dx: float = 1.0
    dy: float = 1.0
    dz: float = 1.0

    def Draw(self):
        shape = BRepPrimAPI_MakeBox(self.dx, self.dy, self.dz).Shape()
        return shape


class Union(BaseGeometry):
    geometries: Tuple[BaseGeometry] = tuple()

    def Draw(self):
        shapes = [geo.GetShape() for geo in self.geometries]
        union = BRepAlgoAPI_Fuse(*shapes)
        return union.Shape()
