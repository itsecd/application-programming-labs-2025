from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

from pathlib import Path
import sys

CURRENT_DIR = Path(__file__).resolve().parent

IMAGE_CRAWLER_DIR = CURRENT_DIR.parent / "lab_2" / "image_crawler"

if str(IMAGE_CRAWLER_DIR) not in sys.path:
    sys.path.insert(0, str(IMAGE_CRAWLER_DIR))

from iterators import ImagePathIterator

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt

from image_viewer import ImageViewer


class MainWindow(QMainWindow):
    """Главное окно приложения для просмотра датасета"""
    
    def __init__(self) -> None:
        super().__init__()
        self.iterator: Optional[ImagePathIterator] = None
        self.current_path: Optional[str] = None
        
        self.init_ui()
        
    def init_ui(self) -> None:
        """Инициализация интерфейса"""
        self.setWindowTitle("Dataset Viewer")
        self.setGeometry(100, 100, 900, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        source_layout = QHBoxLayout()
        
        self.btn_select_folder = QPushButton("Выбрать папку")
        self.btn_select_folder.clicked.connect(self.select_folder)
        source_layout.addWidget(self.btn_select_folder)
        
        self.btn_select_csv = QPushButton("Выбрать CSV")
        self.btn_select_csv.clicked.connect(self.select_csv)
        source_layout.addWidget(self.btn_select_csv)
        
        main_layout.addLayout(source_layout)
        
        self.info_label = QLabel("Выберите папку или CSV файл")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.info_label)
        
        self.image_viewer = ImageViewer()
        main_layout.addWidget(self.image_viewer, stretch=1)
        
        nav_layout = QHBoxLayout()
        
        self.btn_prev = QPushButton("◀ Предыдущее")
        self.btn_prev.clicked.connect(self.show_previous)
        self.btn_prev.setEnabled(False)
        nav_layout.addWidget(self.btn_prev)
        
        self.btn_next = QPushButton("Следующее ▶")
        self.btn_next.clicked.connect(self.show_next)
        self.btn_next.setEnabled(False)
        nav_layout.addWidget(self.btn_next)
        
        main_layout.addLayout(nav_layout)
        
        self.path_label = QLabel("")
        self.path_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.path_label.setWordWrap(True)
        main_layout.addWidget(self.path_label)
        
    def select_folder(self) -> None:
        """Выбор папки с изображениями"""
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с изображениями")
        if folder:
            self.load_source(folder)
            
    def select_csv(self) -> None:
        """Выбор CSV файла с аннотацией"""
        csv_file, _ = QFileDialog.getOpenFileName(
            self, "Выберите CSV файл", "", "CSV Files (*.csv)"
        )
        if csv_file:
            self.load_source(csv_file)
            
    def load_source(self, source: str) -> None:
        """Загрузка источника данных"""
        try:
            self.iterator = ImagePathIterator(source)
            total = len(self.iterator)
            
            source_type = "папка" if Path(source).is_dir() else "CSV"
            self.info_label.setText(f"Загружено из {source_type}: {total} изображений")
            
            self.btn_next.setEnabled(True)
            self.btn_prev.setEnabled(False)
            self.image_viewer.reset()
            self.path_label.setText("")
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить источник:\n{str(e)}")
            
    def show_next(self) -> None:
        """Показать следующее изображение"""
        if not self.iterator:
            return
            
        try:
            self.current_path = next(self.iterator)
            self.display_image(self.current_path)
            self.btn_prev.setEnabled(True)
            
            if self.iterator.index >= len(self.iterator):
                self.btn_next.setEnabled(False)
                
        except StopIteration:
            self.btn_next.setEnabled(False)
            QMessageBox.information(self, "Информация", "Достигнут конец датасета")
            
    def show_previous(self) -> None:
        """Показать предыдущее изображение"""
        if not self.iterator or self.iterator.index <= 1:
            return
            
        self.iterator.index = max(0, self.iterator.index - 2)
        self.show_next()
        
        if self.iterator.index == 1:
            self.btn_prev.setEnabled(False)
            
        self.btn_next.setEnabled(True)
        
    def display_image(self, path: str) -> None:
        """Отображение изображения"""
        try:
            self.image_viewer.load_image(path)
            filename = Path(path).name
            index = self.iterator.index if self.iterator else 0
            total = len(self.iterator) if self.iterator else 0
            self.path_label.setText(f"[{index}/{total}] {filename}\n{path}")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить изображение:\n{str(e)}")