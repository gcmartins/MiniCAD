from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QToolTip, QAction, QStatusBar, QToolBar

from view.components.drawing_canvas import DrawingCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

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
        Create the canvas object that inherits from QLabel.
        """
        self.canvas = DrawingCanvas(self)
        # Set the main window's central widget
        self.setCentralWidget(self.canvas)

    def createMenu(self):
        """
        Set up the menu bar and status bar.
        """
        # Create file menu actions
        new_act = self.createMenuAction(label='New canvas', shortcut='Ctrl+N', action=self.canvas.newCanvas)
        save_file_act = self.createMenuAction(label='Save File', shortcut='Ctrl+S', action=self.canvas.saveFile)
        quit_act = self.createMenuAction(label='Quit', shortcut='Ctrl+Q', action=self.close)
        # Create the menu bar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        # Create file menu and add actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(new_act)
        file_menu.addAction(save_file_act)
        file_menu.addSeparator()
        file_menu.addAction(quit_act)
        # Create tool menu actions
        anti_al_act = QAction('AntiAliasing', self, checkable=True)
        anti_al_act.triggered.connect(self.turnAntialiasingOn)
        # Create tools menu and add actions
        file_menu = menu_bar.addMenu('Tools')
        file_menu.addAction(anti_al_act)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def createMenuAction(self, label: str, shortcut: str, action):
        new_act = QAction(label, self)
        new_act.setShortcut(shortcut)
        new_act.triggered.connect(action)
        return new_act

    def createToolbar(self):
        """
        Create toolbar to contain painting tools.
        """
        tool_bar = QToolBar("Painting Toolbar")
        tool_bar.setIconSize(QSize(24, 24))
        # Set orientation of toolbar to the left side
        self.addToolBar(Qt.LeftToolBarArea, tool_bar)
        tool_bar.setMovable(False)
        # Create actions and tool tips and add them to the toolbar
        pencil_act = QAction(QIcon("view/icons/pencil.png"), 'Pencil', tool_bar)
        pencil_act.setToolTip('This is the <b>Pencil</b>.')
        pencil_act.triggered.connect(lambda: self.canvas.selectDrawingTool("pencil"))
        marker_act = QAction(QIcon("view/icons/marker.png"), 'Marker', tool_bar)
        marker_act.setToolTip('This is the <b>Marker</b>.')
        marker_act.triggered.connect(lambda: self.canvas.selectDrawingTool("marker"))
        eraser_act = QAction(QIcon("view/icons/eraser.png"), "Eraser", tool_bar)
        eraser_act.setToolTip('Use the <b>Eraser</b> to make it all disappear.')
        eraser_act.triggered.connect(lambda: self.canvas.selectDrawingTool("eraser"))
        color_act = QAction(QIcon("view/icons/colors.png"), "Colors", tool_bar)
        color_act.setToolTip('Choose a <b>Color</b> from the Color dialog.')
        color_act.triggered.connect(lambda: self.canvas.selectDrawingTool("color"))
        tool_bar.addAction(pencil_act)
        tool_bar.addAction(marker_act)
        tool_bar.addAction(eraser_act)
        tool_bar.addAction(color_act)

    def turnAntialiasingOn(self, state):
        """
        Turn antialiasing on or off.
        """
        if state:
            self.canvas.antialiasing_status = True
        else:
            self.canvas.antialiasing_status = False

    def leaveEvent(self, event):
        """
        QEvent class that is called when mouse leaves screen's space. Hide mouse coordinates in status bar if mouse leaves
        the window.
        """
        self.canvas.mouse_track_label.setVisible(False)