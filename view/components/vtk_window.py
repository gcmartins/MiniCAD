import vtk
from PyQt5.QtWidgets import QFrame, QVBoxLayout
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkFiltersExtraction import vtkExtractEdges
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkPolyDataMapper, vtkActor, vtkCellPicker


class VtkWindow(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.vl = QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.vl.addWidget(self.vtkWidget)
        self.setLayout(self.vl)

        self.renderer = vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.vtkWidget.GetRenderWindow().GetInteractor()
        style = vtkInteractorStyleTrackballCamera()
        self.interactor.SetInteractorStyle(style)

        self.interactor.Initialize()
        self.show()

    def _SetupExtractEdges(self, source):
        extract_edges = vtkExtractEdges()
        extract_edges.SetInputData(source.GetOutput())
        edge_mapper = vtkPolyDataMapper()
        edge_mapper.SetInputConnection(extract_edges.GetOutputPort())
        edge_actor = vtkActor()
        edge_actor.SetMapper(edge_mapper)
        edge_actor.VisibilityOff()  # set visibility off initially
        self.renderer.AddActor(edge_actor)
        self.selected = False

        # define a function to handle the mouse move event
        def _MoveCallback(obj, event):
            picker = vtkCellPicker()
            pos = self.interactor.GetEventPosition()
            picker.Pick(pos[0], pos[1], 0, self.renderer)
            if not self.selected:
                if picker.GetCellId() != -1:
                    edge_actor.GetProperty().SetColor(1, 0, 0)
                    extract_edges.SetInputData(picker.GetDataSet())
                    edge_actor.VisibilityOn()
                else:
                    edge_actor.VisibilityOff()
                self.interactor.Render()

        # define a function to handle the mouse click event
        def _SelectCallback(obj, event):
            picker = vtkCellPicker()
            pos = self.interactor.GetEventPosition()
            picker.Pick(pos[0], pos[1], 0, self.renderer)
            if picker.GetCellId() != -1:
                if self.selected:
                    self.selected = False
                    edge_actor.VisibilityOff()
                else:
                    edge_actor.GetProperty().SetColor(0, 0, 1)
                    extract_edges.SetInputData(picker.GetDataSet())
                    edge_actor.VisibilityOn()
                    self.selected = True
            self.interactor.Render()

        # attach the move_callback function to the vtkRenderWindowInteractor
        self.interactor.AddObserver("MouseMoveEvent", _MoveCallback)
        self.interactor.AddObserver("LeftButtonPressEvent", _SelectCallback)

    def AddGeometry(self, actor) -> None:
        self.renderer.AddActor(actor)
        self.renderer.ResetCamera()
        self._UpdateView()

    def RemoveGeometry(self, actor):
        self.renderer.RemoveActor(actor)
        self._UpdateView()

    def _UpdateView(self):
        self.vtkWidget.Render()

