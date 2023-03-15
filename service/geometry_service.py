from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Extend.DataExchange import write_stl_file
from vtkmodules.vtkIOGeometry import vtkSTLReader
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper, vtkActor


def stlToActor(fname: str):
    reader = vtkSTLReader()
    reader.SetFileName(fname)
    reader.Update()
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(0.5, 0.5, 1.0)
    return actor


def createSphere(center=(0.0, 0.0, 0.0), radius=1.0):
    sphere = BRepPrimAPI_MakeSphere(radius).Shape()
    return geometryToActor(sphere), sphere


def createCylinder(center=(0.0, 0.0, 0.0), radius=1.3, height=1.0):
    cylinder = BRepPrimAPI_MakeCylinder(radius, height).Shape()
    return geometryToActor(cylinder), cylinder


def createCube(center=(0.0, 0.0, 0.0)):
    cube = BRepPrimAPI_MakeBox(1.0, 1.0, 1.0).Shape()
    return geometryToActor(cube), cube


def geometryToActor(cube):
    write_stl_file(cube, 'output.stl', mode='binary', linear_deflection=0.01)
    return stlToActor('output.stl')


def UnionGeometries(geometries):
    # Perform boolean union operation
    fusedShape = BRepAlgoAPI_Fuse(*geometries).Shape()

    return geometryToActor(fusedShape), fusedShape

