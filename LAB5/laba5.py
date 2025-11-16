import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, 
                             QFileDialog, QWidget, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# Импортируем ваш итератор из второй лабораторной работы
from laba2 import ImageDatasetIterator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dataset_iterator = None
        self.current_file_path = None
        self.all_items = []  # Для хранения всех элементов
        self.current_index = 0  # Текущий индекс
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Просмотр датасета - Лабораторная работа 2')
        self.setGeometry(100, 100, 800, 600)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Кнопки выбора датасета
        button_layout = QHBoxLayout()
        
        self.btn_select_folder = QPushButton('Выбрать папку датасета')
        self.btn_select_folder.clicked.connect(self.select_dataset_folder)
        button_layout.addWidget(self.btn_select_folder)
        
        self.btn_select_annotation = QPushButton('Выбрать файл аннотации')
        self.btn_select_annotation.clicked.connect(self.select_annotation_file)
        button_layout.addWidget(self.btn_select_annotation)
        
        layout.addLayout(button_layout)
        
        # Label для отображения информации о текущем файле
        self.file_info_label = QLabel('Выберите датасет для начала работы')
        self.file_info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.file_info_label)
        
        # Label для отображения изображения
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setText('Изображение будет отображено здесь')
        self.image_label.setStyleSheet('border: 1px solid gray;')
        layout.addWidget(self.image_label)
        
        # Кнопки навигации
        nav_layout = QHBoxLayout()
        
        self.btn_prev = QPushButton('Предыдущее')
        self.btn_prev.clicked.connect(self.previous_item)
        self.btn_prev.setEnabled(False)
        nav_layout.addWidget(self.btn_prev)
        
        self.btn_next = QPushButton('Следующее')
        self.btn_next.clicked.connect(self.next_item)
        self.btn_next.setEnabled(False)
        nav_layout.addWidget(self.btn_next)
        
        layout.addLayout(nav_layout)
        
    def select_dataset_folder(self):
        """Выбор папки с датасетом"""
        folder_path = QFileDialog.getExistingDirectory(
            self, 'Выберите папку с датасетом')
        
        if folder_path:
            try:
                # Создаем итератор для папки
                self.dataset_iterator = ImageDatasetIterator(folder_path=folder_path)
                self.initialize_dataset()
                
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', 
                                   f'Не удалось загрузить датасет: {str(e)}')
    
    def select_annotation_file(self):
        """Выбор файла аннотации"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Выберите файл аннотации', '', 
            'CSV Files (*.csv);;Text Files (*.txt);;All Files (*)')
        
        if file_path:
            try:
                # Создаем итератор для файла аннотации
                self.dataset_iterator = ImageDatasetIterator(annotation_file=file_path)
                self.initialize_dataset()
                
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', 
                                   f'Не удалось загрузить аннотацию: {str(e)}')
    
    def initialize_dataset(self):
        """Инициализация датасета и загрузка всех элементов"""
        if not self.dataset_iterator:
            return
            
        try:
            # Собираем все элементы из итератора
            self.all_items = []
            self.current_index = 0
            
            # Используем итератор для получения всех элементов
            for item in self.dataset_iterator:
                self.all_items.append(item)
            
            if self.all_items:
                self.enable_navigation()
                self.show_current_item()
                self.file_info_label.setText(f'Загружено {len(self.all_items)} изображений')
            else:
                QMessageBox.warning(self, 'Предупреждение', 'Датасет пуст')
                
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', 
                               f'Ошибка при инициализации датасета: {str(e)}')
    
    def enable_navigation(self):
        """Активировать кнопки навигации"""
        self.btn_prev.setEnabled(True)
        self.btn_next.setEnabled(True)
    
    def next_item(self):
        """Показать следующий элемент"""
        if self.all_items and self.current_index < len(self.all_items) - 1:
            self.current_index += 1
            self.show_current_item()
        else:
            QMessageBox.information(self, 'Информация', 'Достигнут конец датасета')
    
    def previous_item(self):
        """Показать предыдущий элемент"""
        if self.all_items and self.current_index > 0:
            self.current_index -= 1
            self.show_current_item()
    
    def show_current_item(self):
        """Показать текущий элемент"""
        if not self.all_items or self.current_index >= len(self.all_items):
            return
            
        item = self.all_items[self.current_index]
        self.display_item(item)
        
        # Обновляем статус кнопок
        self.btn_prev.setEnabled(self.current_index > 0)
        self.btn_next.setEnabled(self.current_index < len(self.all_items) - 1)
    
    def display_item(self, item):
        """Отобразить элемент (изображение)"""
        # Ваш итератор возвращает просто путь к файлу как строку
        file_path = item
        
        self.current_file_path = file_path
        
        if not os.path.exists(file_path):
            self.file_info_label.setText(f'Файл не найден: {file_path}')
            self.image_label.setText('Файл не найден')
            return
        
        # Обновляем информацию о файле
        filename = os.path.basename(file_path)
        self.file_info_label.setText(f'Файл {self.current_index + 1}/{len(self.all_items)}: {filename}')
        
        # Проверяем тип файла и отображаем изображение
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')):
            self.display_image(file_path)
        else:
            # Для не-изображений показываем информацию
            self.image_label.setText(f'Файл: {filename}\n(неподдерживаемый тип)')
    
    def display_image(self, image_path):
        """Отобразить изображение исходного или меньшего размера с сохранением пропорций"""
        try:
            pixmap = QPixmap(image_path)
            
            if pixmap.isNull():
                self.image_label.setText('Не удалось загрузить изображение')
                return
            
            # Получаем размеры label для отображения
            label_width = self.image_label.width()
            label_height = self.image_label.height()
            
            # Получаем исходные размеры изображения
            original_width = pixmap.width()
            original_height = pixmap.height()
            
            # Определяем размер для отображения (меньший или исходный)
            if original_width > label_width or original_height > label_height:
                # Изображение больше label - масштабируем до меньшего размера
                scaled_pixmap = pixmap.scaled(
                    label_width, label_height, 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
            else:
                # Изображение меньше label - используем исходный размер
                scaled_pixmap = pixmap
            
            self.image_label.setPixmap(scaled_pixmap)
            
        except Exception as e:
            self.image_label.setText(f'Ошибка загрузки изображения: {str(e)}')
    
    def resizeEvent(self, event):
        """Обработчик изменения размера окна - перерисовываем изображение"""
        super().resizeEvent(event)
        if (hasattr(self, 'current_file_path') and self.current_file_path and 
            self.current_file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'))):
            self.display_image(self.current_file_path)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()