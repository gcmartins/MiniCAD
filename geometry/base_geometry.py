from typing import Tuple

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Vec, gp_Trsf
from PySide2.QtCore import QObject, Signal


class BaseGeometry(QObject):
    on_geometry_change = Signal()

    name: str = ''
    translation: Tuple[float, float, float] = (0.0, 0.0, 0.0)

    def __init__(self, **kwargs):
        super().__init__()
        for (key, value) in kwargs.items():
            setattr(self, key, value)

    def Draw(self):
        pass

    def GetShape(self):
        shape = self.Draw()
        translation_vector = gp_Vec(*self.translation)

        transformation = gp_Trsf()
        transformation.SetTranslation(translation_vector)

        return BRepBuilderAPI_Transform(shape, transformation, True).Shape()

    def __setattr__(self, key, value):
        if key in self.__dict__ and self.__dict__[key] == value:
            return
        self.__dict__[key] = value
        self.on_geometry_change.emit()
