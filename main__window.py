# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication,QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_DataCheck
from lab_2 import Path_Iterator

class ImageCheck:
    def __init__(self,ui):
        self.ui=ui
        self.iterator=None
        self.signals()
        self.count=0
        self.items=[]
        self.ui.search_line.setPlaceholderText("Введите название источника")

    def signals(self):
        self.ui.search_line.returnPressed.connect(self.select_resourse)
        self.ui.search_button.clicked.connect(self.select_resourse)
        self.ui.next_image.clicked.connect(self.show_next_image)
        self.ui.prev_image.clicked.connect(self.show_prev_image)

    def select_resourse(self):
        name=self.ui.search_line.text()

        if name:
            self.iterator=Path_Iterator(name)
            self.items=list(self.iterator)
            self.count=0
            self.display_image(self.items[0][0])

    def show_next_image(self):
        if self.count<len(self.items)-1:
            self.count+=1
            path=self.items[self.count][0]
            self.display_image(path)

    def show_prev_image(self):
        if self.count>0:
            self.count-=1
            path=self.items[self.count][0]
            self.display_image(path)

    def display_image(self,path):
        image=QPixmap(path)
        widget_width = self.ui.true_proportion.width()
        widget_height = self.ui.true_proportion.height()
        scaled_image=image.scaled(widget_width,widget_height,Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.true_proportion.setPixmap(scaled_image)
        self.ui.true_proportion.repaint()

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DataCheck()
        self.ui.setupUi(self)
        self.viewer = ImageCheck(self.ui)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget=Widget()
    widget.show()
    sys.exit(app.exec())
