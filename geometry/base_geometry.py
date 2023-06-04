from typing import Tuple

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Vec, gp_Trsf
from attr import define


@define(frozen=True)
class BaseGeometry:
    name: str
    translation: Tuple[float, float, float] = (0.0, 0.0, 0.0)

    def Draw(self):
        pass

    def GetShape(self):
        shape = self.Draw()
        translation_vector = gp_Vec(*self.translation)

        transformation = gp_Trsf()
        transformation.SetTranslation(translation_vector)

        return BRepBuilderAPI_Transform(shape, transformation, True).Shape()