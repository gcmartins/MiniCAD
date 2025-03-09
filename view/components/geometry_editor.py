from PySide2.QtGui import QDoubleValidator
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit

from geometry.base_geometry import BaseGeometry
from service.selection_service import SelectionService


class GeometryEditor(QWidget):

    def __init__(self, parent=None, *, selection_service: SelectionService):
        super().__init__(parent)
        self._selection_service = selection_service
        self._selection_service.on_selection_changed.connect(self.SetGeometry)
        self.editor_fields = {}
        self._editor_widget = QWidget(self)

    def SetGeometry(self, geometry: BaseGeometry):
        self._editor_widget.setParent(None)
        self._editor_widget = QWidget(self)
        v_layout = QVBoxLayout(self._editor_widget)
        self._editor_widget.setLayout(v_layout)

        for key, value in geometry.__dict__.items():
            h_layout = QHBoxLayout()
            label = QLabel(key.capitalize())
            h_layout.addWidget(label)

            if isinstance(value, tuple):
                for index, v in enumerate(value):
                    editor = QLineEdit(str(v))
                    validator = QDoubleValidator()
                    validator.setNotation(QDoubleValidator.StandardNotation)
                    validator.setDecimals(10) 
                    editor.setValidator(validator)
                    editor.textChanged.connect(_SetGeometryData(geometry, key, editor, index))
                    h_layout.addWidget(editor)

            else:
                editor = QLineEdit(str(value))
                if isinstance(value, float):
                    validator = QDoubleValidator()
                    validator.setNotation(QDoubleValidator.StandardNotation)
                    validator.setDecimals(10)
                    editor.setValidator(validator)
                editor.textChanged.connect(_SetGeometryData(geometry, key, editor))
                h_layout.addWidget(editor)

            v_layout.addLayout(h_layout)

        self._editor_widget.show()


def _SetGeometryData(geometry, attribute, editor, index=None):

    def callback_function():
        text = editor.text()
        if not text:
            return

        value = getattr(geometry, attribute)
        if isinstance(value, tuple) and index is not None:
            value = list(value)
            value[index] = float(text)
            setattr(geometry, attribute, tuple(value))
        elif isinstance(value, str):
            setattr(geometry, attribute, text)
        elif isinstance(value, float):
            setattr(geometry, attribute, float(text))

    return callback_function
