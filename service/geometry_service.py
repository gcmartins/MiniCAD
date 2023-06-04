from geometry.geometry_models import Sphere, Cylinder, Cube, Union


def createSphere(translation=(0.0, 0.0, 0.0), radius=1.0):
    sphere = Sphere(name='Sphere', radius=radius, translation=translation)
    return sphere


def createCylinder(translation=(0.0, 0.0, 0.0), radius=1.3, height=1.0):
    cylinder = Cylinder(name='Cylinder', radius=radius, height=height, translation=translation)
    return cylinder


def createCube(translation=(0.0, 0.0, 0.0)):
    cube = Cube(name='Cube', dx=1.0, dy=1.0, dz=2.0, translation=translation)
    return cube


def UnionGeometries(geometries, translation=(0.0, 0.0, 0.0)):
    # Perform boolean union operation
    union = Union(name='Union', geometries=tuple(geometries), translation=translation)

    return union

