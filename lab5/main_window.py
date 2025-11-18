# main_window.py
import sys
import os
import csv
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from window_design import Ui_MainWindow
from image_iterator import ImageIterator

class BearViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.image_iterator = None
        self.current_image_path = None
        self.ui.btn_next.clicked.connect(self.next_image)
        self.ui.btn_prev.clicked.connect(self.prev_image)
        self.ui.menu_open.triggered.connect(self.open_annotation)
        self.try_load_annotation()
    
    def try_load_annotation(self):
        """Пробуем загрузить annotation.csv при запуске"""
        if os.path.exists("annotation.csv"):
            self.load_annotation("annotation.csv")
        else:
            self.ui.image_label.setText("Файл annotation.csv не найден\nВыберите файл через меню")
    
    def open_annotation(self):
        """Открыть файл аннотации через диалог"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл аннотации",
            "",
            "CSV Files (*.csv)"
        )
        if file_path:
            self.load_annotation(file_path)
        else:
            # Если выбран каталог вместо файла
            directory = QFileDialog.getExistingDirectory(
                self,
                "Выберите папку с изображениями"
            )
            if directory:
                self.load_directory(directory)
    
    def load_annotation(self, csv_file):
        """Загрузить изображения из CSV файла через итератор"""
        try:
            self.image_iterator = ImageIterator(csv_file)
            self.show_current_image()
            self.update_status(f"Загружено изображений из CSV: {len(self.image_iterator.paths)}")
            
        except Exception as e:
            self.ui.image_label.setText(f"Ошибка загрузки CSV:\n{str(e)}")
            self.image_iterator = None
    
    def load_directory(self, directory):
        """Загрузить изображения из директории через итератор"""
        try:
            self.image_iterator = ImageIterator(directory)
            self.show_current_image()
            self.update_status(f"Загружено изображений из папки: {len(self.image_iterator.paths)}")
            
        except Exception as e:
            self.ui.image_label.setText(f"Ошибка загрузки папки:\n{str(e)}")
            self.image_iterator = None
    
    def next_image(self):
        """Следующее изображение через итератор"""
        if not self.image_iterator or not self.image_iterator.paths:
            return
        
        try:
            # Используем итератор для получения следующего изображения
            self.current_image_path = next(self.image_iterator)
            self.display_image(self.current_image_path)
            self.update_status()
            
        except StopIteration:
            # Достигнут конец - начинаем сначала
            self.image_iterator.counter = 0
            if self.image_iterator.paths:
                self.current_image_path = self.image_iterator.paths[0]
                self.display_image(self.current_image_path)
                self.update_status()
    
    def prev_image(self):
        """Предыдущее изображение через итератор"""
        if not self.image_iterator or not self.image_iterator.paths:
            return
        
        # Для предыдущего изображения просто уменьшаем счетчик
        if self.image_iterator.counter > 0:
            self.image_iterator.counter -= 1
        else:
            # Если в начале - переходим к последнему
            self.image_iterator.counter = len(self.image_iterator.paths) - 1
        
        self.current_image_path = self.image_iterator.paths[self.image_iterator.counter]
        self.display_image(self.current_image_path)
        self.update_status()
    
    def show_current_image(self):
        """Показать текущее изображение через итератор"""
        if not self.image_iterator or not self.image_iterator.paths:
            self.ui.image_label.setText("Нет изображений для отображения")
            return
        
        try:
            # Получаем первое изображение через итератор
            self.current_image_path = next(self.image_iterator)
            self.display_image(self.current_image_path)
            self.update_status()
            
        except StopIteration:
            self.ui.image_label.setText("Нет изображений для отображения")
    
    def display_image(self, image_path):
        """Отобразить изображение по пути"""
        if not os.path.exists(image_path):
            self.ui.image_label.setText(f"Файл не найден:\n{Path(image_path).name}")
            return
        
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self.ui.image_label.setText(f"Ошибка загрузки:\n{Path(image_path).name}")
            return
        
        # Масштабируем изображение
        label_size = self.ui.image_label.size()
        scaled_pixmap = pixmap.scaled(
            label_size.width() - 20,
            label_size.height() - 20,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
        self.ui.image_label.setPixmap(scaled_pixmap)
    
    def update_status(self, message=None):
        """Обновить статусную строку"""
        if message:
            self.ui.status_bar.showMessage(message)
        elif self.image_iterator and self.image_iterator.paths and self.current_image_path:
            current = self.image_iterator.counter
            total = len(self.image_iterator.paths)
            filename = Path(self.current_image_path).name
            self.ui.status_bar.showMessage(f"Изображение {current}/{total} | {filename}")
        else:
            self.ui.status_bar.showMessage("Нет изображений")
    
    def resizeEvent(self, event):
        """При изменении размера окна перерисовываем изображение"""
        super().resizeEvent(event)
        if self.current_image_path:
            self.display_image(self.current_image_path)

def main():
    app = QApplication(sys.argv)
    window = BearViewer()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()