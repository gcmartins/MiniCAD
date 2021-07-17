import sys

from PyQt5.QtWidgets import (QApplication)
from view.main_window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setAttribute(Qt.AA_DontShowIconsInMenus, True)
    MainWindow()
    sys.exit(app.exec_())
