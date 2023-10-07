import os

from PySide2.QtCore import Qt, QPoint, QRect
from PySide2.QtGui import QPixmap, QPainter, QPen, QColor
from PySide2.QtWidgets import QLabel, QColorDialog, QFileDialog


class DrawingCanvas(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        width, height = 900, 600
        self.parent = parent
        self.parent.setFixedSize(width, height)
        # Create pixmap object that will act as the canvas
        pixmap = QPixmap(width, height)  # width, height
        pixmap.fill(Qt.white)
        self.setPixmap(pixmap)
        # Keep track of the mouse for getting mouse coordinates
        self.mouse_track_label = QLabel()
        self.setMouseTracking(True)
        # Initialize variables
        self.antialiasing_status = False
        self.eraser_selected = False
        self.last_mouse_pos = QPoint()
        self.drawing = False
        self.pen_color = Qt.black
        self.pen_width = 2

    def selectDrawingTool(self, tool):
        """
        Determine which tool in the toolbar has been selected.
        """
        if tool == "pencil":
            self.eraser_selected = False
            self.pen_width = 2
        elif tool == "marker":
            self.eraser_selected = False
            self.pen_width = 8
        elif tool == "eraser":
            self.eraser_selected = True
        elif tool == "color":
            self.eraser_selected = False
            color = QColorDialog.getColor()
            if color.isValid():
                self.pen_color = color

    def mouseMoveEvent(self, event):
        """
        Handle mouse movements.
        Track coordinates of mouse in window and display in the status bar.
        """
        mouse_pos = event.pos()
        if (event.buttons() and Qt.LeftButton) and self.drawing:
            self.mouse_pos = event.pos()
            self.drawOnCanvas(mouse_pos)
        self.mouse_track_label.setVisible(True)
        sb_text = "Mouse Coordinates: ({}, {})".format(mouse_pos.x(), mouse_pos.y())
        self.mouse_track_label.setText(sb_text)
        self.parent.status_bar.addWidget(self.mouse_track_label)

    def drawOnCanvas(self, points):
        """
        Performs drawing on canvas.
        """
        painter = QPainter(self.pixmap())
        if self.antialiasing_status:
            painter.setRenderHint(QPainter.Antialiasing)
        if self.eraser_selected == False:
            pen = QPen(QColor(self.pen_color), self.pen_width)
            painter.setPen(pen)
            painter.drawLine(self.last_mouse_pos, points)
            # Update the mouse's position for next movement
            self.last_mouse_pos = points
        elif self.eraser_selected == True:
            # Use the eraser
            eraser = QRect(points.x(), points.y(), 12, 12)
            painter.eraseRect(eraser)
        painter.end()
        self.update()

    def newCanvas(self):
        """
        Clears the current canvas.
        """
        self.pixmap().fill(Qt.white)
        self.update()

    def saveFile(self):
        """
        Save a .png image file of current pixmap area.
        """
        file_format = "png"
        default_name = os.path.curdir + "/untitled." + file_format
        file_name, _ = QFileDialog.getSaveFileName(self, "Save As",
                                                   default_name, "PNG Format (*.png)")
        if file_name:
            self.pixmap().save(file_name, file_format)

    def mousePressEvent(self, event):
        """
        Handle when mouse is pressed.
        """
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()
            self.drawing = True

    def mouseReleaseEvent(self, event):
        """
        Handle when mouse is released.
        Check when eraser is no longer being used.
        """
        if event.button() == Qt.LeftButton:
            self.drawing = False
        elif self.eraser_selected == True:
            self.eraser_selected = False

    def paintEvent(self, event):
        """
        Create QPainter object.
        This is to prevent the chance of the painting being lost
        if the user changes windows.
        """
        painter = QPainter(self)
        target_rect = event.rect()
        painter.drawPixmap(target_rect, self.pixmap(), target_rect)