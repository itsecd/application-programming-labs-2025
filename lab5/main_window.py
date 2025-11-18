# main_window.py
import sys
import os
import csv
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from window_design import Ui_MainWindow

class BearViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.images = []
        self.current_index = 0
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
    
    def load_annotation(self, csv_file):
        """Загрузить изображения из CSV файла"""
        try:
            self.images = []
            
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    # Ищем путь к изображению в колонках
                    if 'absolute_path' in row and row['absolute_path']:
                        path = row['absolute_path']
                        if os.path.exists(path):
                            self.images.append(path)
                    
                    elif 'relative_path' in row and row['relative_path']:
                        rel_path = row['relative_path']
                        abs_path = os.path.join(os.path.dirname(csv_file), rel_path)
                        if os.path.exists(abs_path):
                            self.images.append(abs_path)
            
            if self.images:
                self.current_index = 0
                self.show_current_image()
                self.update_status(f"Загружено {len(self.images)} изображений")
            else:
                self.ui.image_label.setText("В файле не найдено изображений")
                
        except Exception as e:
            self.ui.image_label.setText(f"Ошибка загрузки:\n{str(e)}")
    
    def next_image(self):
        """Следующее изображение"""
        if not self.images:
            return
        self.current_index = (self.current_index + 1) % len(self.images)
        self.show_current_image()
    
    def prev_image(self):
        """Предыдущее изображение"""
        if not self.images:
            return
        self.current_index = (self.current_index - 1) % len(self.images)
        self.show_current_image()
    
    def show_current_image(self):
        """Показать текущее изображение"""
        if not self.images:
            return
            
        image_path = self.images[self.current_index]
        
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
        self.update_status()
    
    def update_status(self, message=None):
        """Обновить статусную строку"""
        if message:
            self.ui.status_bar.showMessage(message)
        elif self.images:
            current = self.current_index + 1
            total = len(self.images)
            filename = Path(self.images[self.current_index]).name
            self.ui.status_bar.showMessage(f"Изображение {current}/{total} | {filename}")
        else:
            self.ui.status_bar.showMessage("Нет изображений")
    
    def resizeEvent(self, event):
        """При изменении размера окна перерисовываем изображение"""
        super().resizeEvent(event)
        if self.images:
            self.show_current_image()

def main():
    app = QApplication(sys.argv)
    window = BearViewer()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()