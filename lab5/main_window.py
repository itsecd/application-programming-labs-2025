import argparse
import sys
import os
import pandas as pd

from PyQt5.QtWidgets import QApplication, QLabel, QTableWidget, QTableWidgetItem, QDialog, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic
from lab2 import FileIterator

class MainWindow(QDialog):
    def __init__(self, filepath: str):
        super().__init__()
        self.filepath = filepath
        self.iterator = None
        self.df = None
        self.current_row = 0
        self.current_image_path = ""
        self.image_label = None
        self.init_ui()

    def init_ui(self):
        """Загрузка интерфейса из .ui файла"""
        uic.loadUi("untitled.ui", self)
        
        self.annotation_button = self.findChild(QPushButton, "annotation_button")
        self.next_button = self.findChild(QPushButton, "next_button")
        self.show_button = self.findChild(QPushButton, "show_button")
        self.table = self.findChild(QTableWidget, "paths_table")
        self.image_label = self.findChild(QLabel, "image_label")
        
        self.annotation_button.clicked.connect(self.load_annotation)
        self.next_button.clicked.connect(self.next_image)
        self.show_button.clicked.connect(self.show_image)

        self.show()

    def load_annotation(self):
        """Загрузка аннотации в таблицу"""
        
        if not self.filepath.endswith(".csv"):
            self.filepath += ".csv"

        if not os.path.exists(self.filepath):
            raise FileNotFoundError("Файл аннотация не найден")
        
        self.df = pd.read_csv(self.filepath)
        self.df.columns = ['absolute_path', 'relative_path']
        self.table.setRowCount(len(self.df))
        self.table.setColumnCount(len(self.df.columns))
        self.table.setHorizontalHeaderLabels(self.df.columns)

        for row_index, row_data in self.df.iterrows():
            item_abs = QTableWidgetItem(str(row_data["absolute_path"]))
            item_rel = QTableWidgetItem(str(row_data["relative_path"]))

            self.table.setItem(row_index, 0, item_abs)    
            self.table.setItem(row_index, 1, item_rel)   

        self.iterator = FileIterator(self.filepath)
        self.table.resizeColumnsToContents()
        self.current_row = 0
        self.table.selectRow(self.current_row)
        next(self.iterator)
        self.current_image_path = next(self.iterator).strip().split(",")[0]
        
    def next_image(self):
        """Переход к следующему изображению"""
        
        if self.iterator is None:
            print("Сначала загрузите аннотацию")
            return
        
        try:
            line = next(self.iterator)
            abs_path = line.strip().split(",")[0]
    
            self.current_image_path = abs_path
            self.current_row += 1
            self.table.selectRow(self.current_row)

        except StopIteration:
            self.iterator = FileIterator(self.filepath)
            self.current_row = 0
            next(self.iterator)
            self.next_image()

    def show_image(self):
        """Показать текущее изображение"""
        if not os.path.exists(self.current_image_path):
            raise FileNotFoundError("Изображения по указанному пути не существует") 
        
        try:
            pixmap = QPixmap(self.current_image_path)

            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                self.image_label.width(), 
                self.image_label.height(),
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
                )
            else:
                self.image_label.setText("Ошибка загрузки изображения!")
                self.image_label.setPixmap(QPixmap())

            self.image_label.setPixmap(pixmap)
        except Exception as e:
            print(f"Ошибка при отображении изображения: {e}")
            self.image_label.setText("Ошибка при отображении!")

def args_parse() -> argparse.Namespace:
    """Эта функция получает аргументы из командной строки"""
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--annotation_file_path", help="Путь к файлу аннотации")

    return parser.parse_args()


def main() -> None:
    annatation_path = args_parse().annotation_file_path
    app = QApplication(sys.argv)
    wind = MainWindow(annatation_path)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()