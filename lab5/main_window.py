import argparse
import sys

from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QApplication,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


from Lab2 import Path_Iterator


def parsing() -> str:
    """передача аргументов через командную строку"""
    parser = argparse.ArgumentParser()
    parser.add_argument("annotation_path", type=str)
    args = parser.parse_args()
    return args.annotation_path


class Gallery(QMainWindow):
    def __init__(self):
        """конструктор класса"""
        super().__init__()
        self.setWindowTitle("Просмотр датасета")
        self.resize(1000, 1000)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.img_label = QLabel("Изображение отсуствует")
        self.img_label.setAlignment(Qt.AlignCenter)
        self.button_next = QPushButton("Следующие изображение")
        self.button_next.setEnabled(False)
        self.button_next.clicked.connect(self.next_img)
        layout.addWidget(self.img_label)
        layout.addWidget(self.button_next)
        self.iterator = None
        self.current_item = None

    def load_annotation(self, annotation_path: str):
        """получение изображений из файла аннотации"""
        self.iterator = Path_Iterator(annotation_path)
        self.iterator.index = 0
        self.current_item = next(self.iterator)
        self.show_img(self.current_item)
        self.button_next.setEnabled(True)

    def show_img(self, file_path:str):
        """Отображение изображений"""
        path = file_path
        img = QPixmap(path)
        img = img.scaled(800, 800, 
                 Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.img_label.setPixmap(img)
        self.img_label.setText("")

    def next_img(self):
        """Переход к следующему изображению"""
        if self.iterator is None:
            return
        try:
            self.current_item = next(self.iterator)
            self.show_img(self.current_item)
        except StopIteration:
            self.button_next.setEnabled(False)


def main():
    try:
        annotation_path = parsing()
        app = QApplication(sys.argv)
        gallery = Gallery()
        gallery.load_annotation(annotation_path)
        gallery.show()
        sys.exit(app.exec())
    except Exception as ex:
        print("Ошибка: ", ex)


if __name__ == "__main__":
    main()
