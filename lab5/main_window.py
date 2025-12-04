import sys
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QFileDialog
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from main import ImagePathIterator


class Gallery(QMainWindow):
    """Класс главного окна для просмотра датасета изображений из CSV аннотации."""
    
    def __init__(self) -> None:
        """Инициализирует главное окно приложения."""
        super().__init__()
        self.setWindowTitle("Просмотр датасета")
        self.resize(800, 600)
        
        self.iterator: Optional[ImagePathIterator] = None
        self.current_index: int = 0
        
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Настраивает пользовательский интерфейс."""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)
        
        self.btn_load_csv = QPushButton("Загрузить CSV аннотацию")
        self.btn_load_csv.clicked.connect(self._load_csv)
        
        self.btn_next = QPushButton("Следующее изображение")
        self.btn_next.setEnabled(False)
        self.btn_next.clicked.connect(self._next_image)
        
        self.img_label = QLabel("Выберите файл аннотации CSV")
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.info_label = QLabel("")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.btn_load_csv)
        layout.addWidget(self.img_label, 1)
        layout.addWidget(self.info_label)
        layout.addWidget(self.btn_next)
    
    def _load_csv(self) -> None:
        """Загружает CSV файл аннотации и отображает первое изображение."""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Выберите CSV файл аннотации", "", "CSV Files(*.csv)"
            )
            
            if file_path:
                self.iterator = ImagePathIterator(file_path)
                
                if self.iterator._items:
                    self.current_index = 0
                    self.btn_next.setEnabled(True)
                    self._update_display()
                else:
                    self.img_label.setText("CSV файл не содержит изображений")
        except Exception as ex:
            self.img_label.setText(f"Ошибка загрузки CSV: {ex}")
    
    def _update_display(self) -> None:
        """Обновляет отображение текущего изображения и информации."""
        if self.iterator and self.iterator._items:
            total = len(self.iterator._items)
            current_num = self.current_index + 1
            self.info_label.setText(f"Изображение {current_num} из {total}")
            
            abs_path = self.iterator._items[self.current_index][0]
            pixmap = QPixmap(abs_path)
            
            if pixmap.isNull():
                self.img_label.setText(f"Не удалось загрузить: {Path(abs_path).name}")
            else:
                scaled = pixmap.scaled(
                    self.img_label.size().width() - 50,
                    self.img_label.size().height() - 50,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.img_label.setPixmap(scaled)
    
    def _next_image(self) -> None:
        """Переходит к следующему изображению в датасете."""
        if self.iterator and self.iterator._items:
            self.current_index = (self.current_index + 1) % len(self.iterator._items)
            self._update_display()
    
    def resizeEvent(self, event) -> None:
        """
        Обрабатывает событие изменения размера окна.
        """
        super().resizeEvent(event)
        if self.iterator and self.iterator._items:
            self._update_display()


def main() -> None:
    """Главная функция для запуска приложения."""
    try:
        app = QApplication(sys.argv)
        gallery = Gallery()
        gallery.show()
        sys.exit(app.exec())
    except Exception as ex:
        print(f"Ошибка: {ex}")


if __name__ == "__main__":
    main()