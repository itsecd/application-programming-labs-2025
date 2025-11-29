import os
import sys

from file_iterator import FileIterator

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QPixmap, QResizeEvent
from PyQt5.QtWidgets import (
    QApplication, QFileDialog, QHBoxLayout, QLabel, QMainWindow,
    QMessageBox, QPushButton, QVBoxLayout, QWidget)


window_width = 800
window_heights = 650


class MainWindow(QMainWindow):
    """
    Главное окно приложения для просмотра датасета изображений.
    """

    def __init__(self: QMainWindow) -> None:
        super().__init__()

        self.iterator = None
        self.current_pixmap = None
        self.next_button = None
        self.select_file_button = None
        self.image_label = None
        self.status_bar = None

    def _setup_ui(self: QMainWindow) -> None:
        pass

    def select_annotation_file(self) -> None:
        pass

    def load_next_image(self) -> None:
        pass

    def _display_image(self, path: str) -> None:
        pass

    def _scale_and_set_pixmap(self) -> None:
        pass

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)


def main()-> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()