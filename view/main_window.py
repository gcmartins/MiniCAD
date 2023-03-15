from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QToolTip, QAction, QStatusBar, QToolBar

from service.geometry_service import createSphere, createCylinder, UnionGeometries, createCube
from view.components.vtk_window import VtkWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.geometries = []
        self.geo_sources = []

    def initializeUI(self):
        """
        Initialize the window and display its contents to the screen.
        """
        # self.setMinimumSize(700, 600)
        self.setWindowTitle('Python CAD')
        QToolTip.setFont(QFont('Helvetica', 12))
        self.createCanvas()
        self.createMenu()
        self.createToolbar()
        self.show()

    def createCanvas(self):
        """
        Create the canvas object that inherits from QFrame.
        """
        self.canvas = VtkWindow(self)
        # Set the main window's central widget
        self.setCentralWidget(self.canvas)

    def createMenu(self):
        """
        Set up the menu bar and status bar.
        """
        # Create file menu actions
        # new_act = self.createMenuAction(label='New canvas', shortcut='Ctrl+N', action=self.canvas.newCanvas)
        # save_file_act = self.createMenuAction(label='Save File', shortcut='Ctrl+S', action=self.canvas.saveFile)
        quit_act = self.createMenuAction(label='Quit', shortcut='Ctrl+Q', action=self.close)
        # Create the menu bar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        # Create file menu and add actions
        file_menu = menu_bar.addMenu('File')
        # file_menu.addAction(new_act)
        # file_menu.addAction(save_file_act)
        # file_menu.addSeparator()
        file_menu.addAction(quit_act)
        # Create tools menu and add actions
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def createMenuAction(self, label: str, shortcut: str, action):
        new_act = QAction(label, self)
        new_act.setShortcut(shortcut)
        new_act.triggered.connect(action)
        return new_act

    def createToolbar(self):
        """
        Create toolbar to contain drawing tools.
        """
        tool_bar = QToolBar("Draw Toolbar", self)
        tool_bar.setIconSize(QSize(24, 24))
        # Set orientation of toolbar to the left side
        self.addToolBar(Qt.LeftToolBarArea, tool_bar)
        tool_bar.setMovable(False)
        # Create actions and tool tips and add them to the toolbar
        action = QAction(QIcon("view/icons/sphere.png"), 'Sphere', tool_bar)
        action.setToolTip('Create <b>Sphere</b>.')
        action.triggered.connect(self.AddSphere)
        tool_bar.addAction(action)

        action = QAction(QIcon("view/icons/cylinder.png"), 'Cylinder', tool_bar)
        action.setToolTip('Create <b>Cone</b>.')
        action.triggered.connect(self.AddCylinder)
        tool_bar.addAction(action)

        action = QAction(QIcon("view/icons/cube.png"), 'Cube', tool_bar)
        action.setToolTip('Create <b>Cube</b>.')
        action.triggered.connect(self.AddCube)
        tool_bar.addAction(action)

        action = QAction(QIcon("view/icons/eraser.png"), "Eraser", tool_bar)
        action.setToolTip('Erase all geometries.')
        action.triggered.connect(self.DeleteGeometries)
        tool_bar.addAction(action)

        action = QAction(QIcon("view/icons/colors.png"), "Colors", tool_bar)
        action.setToolTip('Perform <b>Union</b> of the geometries.')
        action.triggered.connect(lambda: self.UnionGeometries())
        tool_bar.addAction(action)

    def AddSphere(self):
        actor, source = createSphere()
        self.canvas.AddGeometry(actor)
        self.AddGeometry(actor, source)

    def AddCylinder(self):
        actor, source = createCylinder()
        self.canvas.AddGeometry(actor)
        self.AddGeometry(actor, source)

    def AddCube(self):
        actor, source = createCube()
        self.canvas.AddGeometry(actor)
        self.AddGeometry(actor, source)

    def AddGeometry(self, actor, source):
        self.geometries.append(actor)
        self.geo_sources.append(source)

    def DeleteGeometries(self):
        for geometry in self.geometries:
            self.canvas.RemoveGeometry(geometry)
        self.geometries = []
        self.geo_sources = []

    def UnionGeometries(self):
        actor, source = UnionGeometries(self.geo_sources)
        self.DeleteGeometries()
        self.canvas.AddGeometry(actor)
        self.AddGeometry(actor, source)
        print(self.geometries)

