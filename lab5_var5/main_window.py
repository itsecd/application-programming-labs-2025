"""Главное окно приложения для просмотра датасета."""
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QWidget, QFileDialog, QMessageBox,
                             QFrame, QSizePolicy)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from dataset_iterator import DatasetIterator


class ImageViewer(QMainWindow):
    """Главное окно просмотрщика изображений."""
    
    def __init__(self):
        """Инициализация главного окна."""
        super().__init__()
        self.dataset_iterator = None
        self.init_ui()
        
        # Автоматическая загрузка датасета при запуске
        self.load_default_dataset()
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        self.setWindowTitle("Просмотрщик датасета птиц")
        self.setMinimumSize(800, 600)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный layout
        main_layout = QVBoxLayout(central_widget)
        
        # Панель управления
        control_layout = QHBoxLayout()
        
        self.btn_load_folder = QPushButton("Загрузить папку")
        self.btn_load_folder.clicked.connect(self.load_folder)
        
        self.btn_load_annotation = QPushButton("Загрузить аннотацию")
        self.btn_load_annotation.clicked.connect(self.load_annotation)
        
        self.btn_prev = QPushButton("← Назад")
        self.btn_prev.clicked.connect(self.show_previous)
        
        self.btn_next = QPushButton("Вперед →")
        self.btn_next.clicked.connect(self.show_next)
        
        control_layout.addWidget(self.btn_load_folder)
        control_layout.addWidget(self.btn_load_annotation)
        control_layout.addStretch()
        control_layout.addWidget(self.btn_prev)
        control_layout.addWidget(self.btn_next)
        
        # Метка информации
        self.lbl_info = QLabel("Загрузите датасет для начала просмотра")
        self.lbl_info.setAlignment(Qt.AlignCenter)
        
        # Область для изображения
        self.image_frame = QFrame()
        self.image_frame.setFrameStyle(QFrame.Box)
        self.image_frame.setMinimumSize(400, 300)
        
        image_layout = QVBoxLayout(self.image_frame)
        
        self.lbl_image = QLabel()
        self.lbl_image.setAlignment(Qt.AlignCenter)
        self.lbl_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lbl_image.setMinimumSize(200, 150)
        self.lbl_image.setText("Изображение не загружено")
        
        image_layout.addWidget(self.lbl_image)
        
        # Добавляем все в главный layout
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.lbl_info)
        main_layout.addWidget(self.image_frame, 1)
        
        # Инициализируем состояние кнопок
        self.update_buttons_state()
    
    def load_default_dataset(self):
        """Загрузка датасета по умолчанию."""
        annotation_file = r"C:\Users\gayvo\OneDrive\Desktop\pp\lab2\annotation.csv"
        dataset_dir = r"C:\Users\gayvo\OneDrive\Desktop\pp\lab2\bird_images"
        
        try:
            if os.path.exists(annotation_file):
                self.load_annotation_file(annotation_file)
            elif os.path.exists(dataset_dir):
                self.load_dataset_folder(dataset_dir)
            else:
                # Если датасет не найден, отключаем кнопки навигации
                self.update_buttons_state()
        except Exception as e:
            print(f"Ошибка при загрузке датасета по умолчанию: {e}")
            self.update_buttons_state()
    
    def load_folder(self):
        """Загрузка датасета из папки."""
        folder = QFileDialog.getExistingDirectory(
            self, "Выберите папку с изображениями", 
            r"C:\Users\gayvo\OneDrive\Desktop\pp\lab2"
        )
        
        if folder:
            self.load_dataset_folder(folder)
    
    def load_annotation(self):
        """Загрузка датасета из файла аннотации."""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл аннотации", 
            r"C:\Users\gayvo\OneDrive\Desktop\pp\lab2",
            "CSV Files (*.csv)"
        )
        
        if file_name:
            self.load_annotation_file(file_name)
    
    def load_dataset_folder(self, folder_path):
        """Загрузка датасета из папки."""
        try:
            self.dataset_iterator = DatasetIterator(dataset_dir=folder_path)
            if len(self.dataset_iterator) > 0:
                self.show_current_image()
                self.update_info("Датасет загружен из папки")
            else:
                QMessageBox.warning(self, "Ошибка", "В выбранной папке нет изображений")
                self.update_buttons_state()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить датасет: {str(e)}")
            self.update_buttons_state()
    
    def load_annotation_file(self, annotation_file):
        """Загрузка датасета из файла аннотации."""
        try:
            self.dataset_iterator = DatasetIterator(annotation_file=annotation_file)
            if len(self.dataset_iterator) > 0:
                self.show_current_image()
                self.update_info("Датасет загружен из аннотации")
            else:
                QMessageBox.warning(self, "Ошибка", "В файле аннотации нет данных")
                self.update_buttons_state()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить аннотацию: {str(e)}")
            self.update_buttons_state()
    
    def show_current_image(self):
        """Отображение текущего изображения."""
        if not self.dataset_iterator or len(self.dataset_iterator) == 0:
            return
        
        image_path = self.dataset_iterator.get_current()
        
        if not os.path.exists(image_path):
            self.lbl_image.setText(f"Файл не найден:\n{image_path}")
            return
        
        # Загрузка и отображение изображения
        pixmap = QPixmap(image_path)
        
        if pixmap.isNull():
            self.lbl_image.setText(f"Не удалось загрузить изображение:\n{image_path}")
            return
        
        # Масштабирование изображения с сохранением пропорций
        scaled_pixmap = self.scale_pixmap(pixmap)
        self.lbl_image.setPixmap(scaled_pixmap)
        
        # Обновление информации
        self.update_info()
        
        # Обновление состояния кнопок
        self.update_buttons_state()
    
    def scale_pixmap(self, pixmap):
        """
        Масштабирование QPixmap с сохранением пропорций.
        
        Args:
            pixmap: Исходное изображение
            
        Returns:
            QPixmap: Масштабированное изображение
        """
        # Получаем размеры области отображения
        label_size = self.lbl_image.size()
        label_width = label_size.width() - 20  # Отступы
        label_height = label_size.height() - 20
        
        # Получаем размеры исходного изображения
        original_size = pixmap.size()
        original_width = original_size.width()
        original_height = original_size.height()
        
        # Вычисляем коэффициенты масштабирования
        width_ratio = label_width / original_width
        height_ratio = label_height / original_height
        
        # Используем меньший коэффициент для сохранения пропорций
        scale_ratio = min(width_ratio, height_ratio, 1.0)  # Не увеличиваем изображение
        
        # Вычисляем новые размеры
        new_width = int(original_width * scale_ratio)
        new_height = int(original_height * scale_ratio)
        
        # Масштабируем изображение
        return pixmap.scaled(
            new_width, new_height, 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
    
    def show_next(self):
        """Показать следующее изображение."""
        if self.dataset_iterator and len(self.dataset_iterator) > 0:
            self.dataset_iterator.next()
            self.show_current_image()
    
    def show_previous(self):
        """Показать предыдущее изображение."""
        if self.dataset_iterator and len(self.dataset_iterator) > 0:
            self.dataset_iterator.prev()
            self.show_current_image()
    
    def update_info(self, custom_message=None):
        """Обновление информационной метки."""
        if custom_message:
            self.lbl_info.setText(custom_message)
        elif self.dataset_iterator and len(self.dataset_iterator) > 0:
            current_idx = self.dataset_iterator.get_current_index() + 1
            total = self.dataset_iterator.get_total_count()
            image_path = self.dataset_iterator.get_current()
            file_name = os.path.basename(image_path)
            
            info_text = f"Изображение {current_idx} из {total} | Файл: {file_name}"
            self.lbl_info.setText(info_text)
        else:
            self.lbl_info.setText("Загрузите датасет для начала просмотра")
    
    def update_buttons_state(self):
        """Обновление состояния кнопок."""
        # Явно проверяем наличие данных и преобразуем в булево значение
        has_data = False
        if self.dataset_iterator and hasattr(self.dataset_iterator, '__len__'):
            try:
                has_data = len(self.dataset_iterator) > 0
            except:
                has_data = False
        
        # Устанавливаем состояние кнопок
        self.btn_prev.setEnabled(bool(has_data))
        self.btn_next.setEnabled(bool(has_data))
    
    def resizeEvent(self, event):
        """Обработчик изменения размера окна."""
        super().resizeEvent(event)
        # При изменении размера окна перерисовываем изображение
        if self.dataset_iterator and len(self.dataset_iterator) > 0:
            self.show_current_image()


def main():
    """Запуск приложения."""
    app = QApplication(sys.argv)
    
    viewer = ImageViewer()
    viewer.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()