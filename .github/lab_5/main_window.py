import sys
import os
import argparse


import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QLabel, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QMainWindow, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

current_dir = os.path.dirname(os.path.abspath(__file__))
lab_2_dir = os.path.join(os.path.dirname(current_dir), 'lab_2')

if lab_2_dir not in sys.path:
    sys.path.insert(0, lab_2_dir)

from lab2 import MyIterator

class MainWindow(QMainWindow):

    def __init__(self, filepath: str):
        super().__init__()
        self.initUI(filepath)


    def initUI(self, filepath: str):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QHBoxLayout(self.central_widget)

        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self.central_layout.addWidget(self.widget)

        self.qbtn = QPushButton('Показать Датафрейм')
        self.qbtn.clicked.connect(lambda: [self.show_df(filepath), self.qbtn.deleteLater()])
        self.layout.addWidget(self.qbtn)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.btns = QWidget()
        self.btns_layout = QHBoxLayout(self.btns)
        self.btn1 = QPushButton('Показать')
        self.btn2 = QPushButton('Далее')
        self.btns_layout.addWidget(self.btn1)
        self.btns_layout.addWidget(self.btn2)
        self.layout.addWidget(self.btns)
        self.btns.hide()

        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.setMinimumSize(500, 400)
        self.img_label.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0;")
        self.img_label.setText("Изображение появится здесь")
        self.central_layout.addWidget(self.img_label)

        self.setGeometry(300, 300, 1000, 1000)
        self.setWindowTitle('My app')
        self.show()


    def show_df(self,  filepath: str):
        try:
            if(not filepath.endswith(".csv")):
                filepath += ".csv"
            df = pd.read_csv(filepath, index_col=0)

            self.table.setRowCount(len(df))
            self.table.setColumnCount(len(df.columns))
            self.table.setHorizontalHeaderLabels(df.columns)

            for row_index, row_data in df.iterrows():
                for col_index, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    self.table.setItem(row_index, col_index, item)
            self.table.resizeColumnsToContents()
            self.id = 0
            self.table.selectRow(self.id)
            self.iterator = MyIterator(filepath)

            next(self.iterator)
            line = next(self.iterator)
            self.path = line.split(',')[1]

            self.btns.show()
            self.btn1.clicked.connect(self.show_img)
            self.btn2.clicked.connect(self.next_row)
        except Exception as e:
            raise Exception(f"Error reading {e}")


    def next_row(self):
        try:
            line = next(self.iterator)
            self.path = line.split(',')[1]
            self.id = self.id + 1
            self.table.selectRow(self.id)
        except StopIteration:
            self.id = 0
            self.table.selectRow(self.id)
            self.iterator = MyIterator(self.iterator.filepath)
            next(self.iterator)

    
    def show_img(self):
        pixmap = QPixmap(self.path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(500, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.img_label.setPixmap(pixmap)
            self.img_label.setText('')
        else:
            self.img_label.setText('Картинка не найдена!')
            self.img_label.setPixmap(QPixmap())
    

def main():
    parser = argparse.ArgumentParser(description="Извлечение данных из файла на основе шаблонов.")
    parser.add_argument("--csvfile", "-c", default="df.csv", type=str, help="Путь к csv файлу.")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    ex = MainWindow(args.csvfile)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()