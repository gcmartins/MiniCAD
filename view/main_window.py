from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QFont, QIcon
from PySide2.QtWidgets import QMainWindow, QToolTip, QAction, QStatusBar, QToolBar, QSplitter

from service.geometry_service import GeometryCollection
from service.selection_service import SelectionService
from view.components.geometry_editor import GeometryEditor
from view.components.occ_window import OCCWindow
from view.components.tree_widget import GeometryTreeWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.geometry_collection = GeometryCollection()
        self.selection_service = SelectionService()
        self.initializeUI()

    def initializeUI(self):
        """
        Initialize the window and display its contents to the screen.
        """
        # self.setMinimumSize(700, 600)
        self.showMaximized()
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
        self.canvas = OCCWindow(self, self.geometry_collection)

        # Create a tree widget and add some items to it
        self.tree = GeometryTreeWidget(self, self.geometry_collection, self.selection_service)

        self.editor = GeometryEditor(self, selection_service=self.selection_service)

        # Create a splitter widget to contain the tree widget and 3D viewer widget
        splitter = QSplitter(Qt.Horizontal)

        v_splitter = QSplitter(Qt.Vertical)
        v_splitter.addWidget(self.tree)
        v_splitter.addWidget(self.editor)
        v_splitter.setSizes([700, 300])

        splitter.addWidget(v_splitter)
        splitter.addWidget(self.canvas)
        splitter.setSizes([350, 650])

        # Set the main window's central widget
        self.setCentralWidget(splitter)

    def createMenu(self):
        """
        Set up the menu bar and status bar.
        """
        # Create file menu actions
        quit_act = self.createMenuAction(label='Quit', shortcut='Ctrl+Q', action=self.close)
        # Create the menu bar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        # Create file menu and add actions
        file_menu = menu_bar.addMenu('File')
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
        self.geometry_collection.createSphere()

    def AddCylinder(self):
        self.geometry_collection.createCylinder()

    def AddCube(self):
        self.geometry_collection.createCube()

    def DeleteGeometries(self):
        pass

    def UnionGeometries(self):
        self.geometry_collection.unionGeometries()

