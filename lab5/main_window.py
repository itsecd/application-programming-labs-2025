import sys
import os
import csv
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

#Импортирую image_iterator
try:
    from image_iterator import ImageIterator
    HAS_ITERATOR = True
    print("ImageIterator найден")
except ImportError:
    HAS_ITERATOR = False
    print("ImageIterator не найден, используется режим совместимости")

# Импортирую сгенерированный интерфейс
from ui_main_window import Ui_MainWindow

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Загружаю интерфейс из .ui файла
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        
        self.image_paths = []
        self.current_index = 0
        
        
        self.ui.pushButton.clicked.connect(self.next_image)  
        self.ui.pushButton_2.clicked.connect(self.previous_image)  
        self.ui.actionSelectSource.triggered.connect(self.select_source)
        
        self.setup_display()
        
        self.auto_load_annotation()
    
    def setup_display(self):
        """Дополнительная настройка отображения"""
        self.ui.label.clear()
        self.ui.label.setText("Загрузка...")
        
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_2.setEnabled(False)
    
    def auto_load_annotation(self):
        """Автоматическая загрузка annotation.csv при запуске"""
        csv_path = "annotation.csv"
        
        if os.path.exists(csv_path):
            print(f"Найден файл аннотации: {csv_path}")
            self.load_csv_source(csv_path)
        else:
            self.ui.label.setText("Файл annotation.csv не найден.\nВыберите источник через меню 'Файл'")
            print("Файл annotation.csv не найден")
    
    def select_source(self):
        """Выбор источника данных"""
        choice = QMessageBox.question(
            self,
            "Выбор источника",
            "Выберите тип источника данных:\n\n"
            "Да - CSV файл аннотации\n"
            "Нет - Папка с изображениями",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if choice == QMessageBox.Yes:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Выберите CSV файл аннотации",
                "",
                "CSV Files (*.csv)"
            )
            if file_path:
                self.load_csv_source(file_path)
                
        elif choice == QMessageBox.No:
            folder_path = QFileDialog.getExistingDirectory(
                self,
                "Выберите папку с изображениями"
            )
            if folder_path:
                self.load_folder_source(folder_path)
    
    def load_csv_source(self, csv_path):
        """Загрузка данных из CSV файла"""
        try:
            if HAS_ITERATOR:
                self.image_iterator = ImageIterator(csv_path)
                self.image_paths = self.image_iterator.paths
            else:
                self.image_paths = self.load_csv_manual(csv_path)
            
            if self.image_paths:
                self.current_index = 0
                self.enable_navigation()
                self.display_current_image()
                self.update_status(f"Загружено {len(self.image_paths)} изображений из CSV")
                print(f"Успешно загружено {len(self.image_paths)} путей к изображениям")
            else:
                QMessageBox.warning(self, "Предупреждение", "Не найдено доступных изображений")
                self.ui.label.setText("Не найдено доступных изображений")
                
        except Exception as e:
            error_msg = f"Ошибка загрузки CSV: {str(e)}"
            QMessageBox.critical(self, "Ошибка", error_msg)
            self.ui.label.setText(f"Ошибка:\n{str(e)}")
            print(error_msg)
    
    def load_csv_manual(self, csv_path):
        """Ручная загрузка CSV файла с поиском изображений"""
        paths = []
        found_images = 0
        missing_images = 0
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row_num, row in enumerate(reader, 1):
                    if 'absolute_path' in row and row['absolute_path']:
                        abs_path = row['absolute_path']
                        
                        if os.path.exists(abs_path):
                            paths.append(abs_path)
                            found_images += 1
                            print(f"✓ Найдено: {Path(abs_path).name}")
                        else:
                            missing_images += 1
                            print(f"✗ Не найден: {abs_path}")
                            
                            file_name = Path(abs_path).name
                            local_path = os.path.join(os.path.dirname(csv_path), file_name)
                            if os.path.exists(local_path):
                                paths.append(local_path)
                                found_images += 1
                                print(f"✓ Найден локально: {file_name}")
                    
                    elif 'relative_path' in row and row['relative_path']:
                        rel_path = row['relative_path']
                        base_dir = os.path.dirname(csv_path)
                        abs_path = os.path.join(base_dir, rel_path)
                        
                        if os.path.exists(abs_path):
                            paths.append(abs_path)
                            found_images += 1
                            print(f"✓ Найдено: {rel_path}")
                        else:
                            missing_images += 1
                            print(f"✗ Не найден: {abs_path}")
            
            print(f"Итог: найдено {found_images}, отсутствует {missing_images} изображений")
            
            if not paths:
                csv_dir = os.path.dirname(csv_path)
                paths = self.find_images_in_directory(csv_dir)
                print(f"Найдено {len(paths)} изображений в папке с CSV")
                
        except Exception as e:
            print(f"Ошибка чтения CSV: {e}")
           
            csv_dir = os.path.dirname(csv_path)
            paths = self.find_images_in_directory(csv_dir)
        
        return paths
    
    def load_folder_source(self, folder_path):
        """Загрузка изображений из папки"""
        try:
            if HAS_ITERATOR:
                self.image_iterator = ImageIterator(folder_path)
                self.image_paths = self.image_iterator.paths
            else:
                self.image_paths = self.find_images_in_directory(folder_path)
            
            if self.image_paths:
                self.current_index = 0
                self.enable_navigation()
                self.display_current_image()
                self.update_status(f"Загружено {len(self.image_paths)} изображений из папки")
            else:
                QMessageBox.warning(self, "Предупреждение", "В папке не найдено изображений")
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки папки: {str(e)}")
    
    def find_images_in_directory(self, directory):
        """Поиск изображений в директории"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        paths = []
        
        try:
            for file_name in os.listdir(directory):
                file_path = os.path.join(directory, file_name)
                if os.path.isfile(file_path):
                    file_ext = os.path.splitext(file_name)[1].lower()
                    if file_ext in image_extensions:
                        paths.append(file_path)
        except Exception as e:
            print(f"Ошибка поиска изображений: {e}")
        
        return paths
    
    def enable_navigation(self):
        """Активация кнопок навигации"""
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton_2.setEnabled(True)
    
    def next_image(self):
        """Следующее изображение"""
        if not self.image_paths:
            return
        
        self.current_index = (self.current_index + 1) % len(self.image_paths)
        self.display_current_image()
    
    def previous_image(self):
        """Предыдущее изображение"""
        if not self.image_paths:
            return
        
        self.current_index = (self.current_index - 1) % len(self.image_paths)
        self.display_current_image()
    
    def display_current_image(self):
        """Отображение текущего изображения"""
        if not self.image_paths or self.current_index >= len(self.image_paths):
            return
        
        try:
            image_path = self.image_paths[self.current_index]
            
            if not os.path.exists(image_path):
                self.ui.label.setText(f"Файл не найден:\n{Path(image_path).name}")
                print(f"Файл не существует: {image_path}")
                return
            
            pixmap = QPixmap(image_path)
            
            if pixmap.isNull():
                self.ui.label.setText(f"Ошибка загрузки:\n{Path(image_path).name}")
                print(f"Не удалось загрузить изображение: {image_path}")
                return
            
            label_size = self.ui.label.size()
            scaled_pixmap = pixmap.scaled(
                label_size.width() - 20,
                label_size.height() - 20,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            self.ui.label.setPixmap(scaled_pixmap)
            self.update_status()
            print(f"Отображено: {Path(image_path).name}")
            
        except Exception as e:
            error_text = f"Ошибка загрузки:\n{str(e)}"
            self.ui.label.setText(error_text)
            print(f"Ошибка: {e}")
    
    def update_status(self, custom_message=None):
        """Обновление статусной строки"""
        if custom_message:
            self.ui.statusbar.showMessage(custom_message)
        elif self.image_paths:
            total = len(self.image_paths)
            current = self.current_index + 1
            if self.current_index < len(self.image_paths):
                current_file = Path(self.image_paths[self.current_index]).name
            else:
                current_file = "N/A"
            
            status_text = f"Изображение {current}/{total} | Файл: {current_file}"
            self.ui.statusbar.showMessage(status_text)
        else:
            self.ui.statusbar.showMessage("Нет загруженных изображений")
    
    def resizeEvent(self, event):
        """Обработчик изменения размера окна"""
        super().resizeEvent(event)
        if self.image_paths:
            self.display_current_image()

def main():
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()