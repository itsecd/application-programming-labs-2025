from __future__ import annotations
import os
import sys
from typing import Optional
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)
from image_iterator import ImageIterator

class DatasetViewer(QMainWindow):
    """
    Главное окно приложения для просмотра изображений из датасета.

    Поддерживает загрузку данных через CSV-аннотацию или напрямую из папки.
    Использует кастомный итератор ImageIterator из лабораторной работы №2.
    """

    def __init__(self) -> None:
        """Инициализирует главное окно и интерфейс."""
        super().__init__()

        self.setWindowTitle("Лабораторная работа №5 — Просмотрщик датасета")
        self.setGeometry(100, 100, 1100, 750)

        self.iterator: Optional[ImageIterator] = None
        self.current_path: Optional[str] = None

        self.init_ui()

    def init_ui(self) -> None:
        """Создаёт и настраивает все элементы интерфейса."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.image_label = QLabel("Нажмите «Открыть датасет», чтобы начать")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #f8f8f8;
                border: 3px dashed #888;
                border-radius: 12px;
                font-size: 18px;
                color: #555;
                padding: 20px;
            }
        """)
        self.image_label.setMinimumHeight(500)
        main_layout.addWidget(self.image_label)

    
        button_layout = QHBoxLayout()

        self.btn_open = QPushButton("Открыть датасет (CSV или папку)")
        self.btn_open.clicked.connect(self.open_dataset)
        self.btn_open.setStyleSheet("QPushButton { padding: 10px 20px; font-size: 14px; }")

        self.btn_prev = QPushButton("Предыдущее")
        self.btn_prev.clicked.connect(self.show_previous)
        self.btn_prev.setEnabled(False)

        self.btn_next = QPushButton("Следующее")
        self.btn_next.clicked.connect(self.show_next)
        self.btn_next.setEnabled(False)

        button_layout.addWidget(self.btn_open)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_prev)
        button_layout.addWidget(self.btn_next)
        main_layout.addLayout(button_layout)


        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов. Откройте CSV-файл или папку с изображениями.")

    def open_dataset(self) -> None:
        """
        Открывает диалог выбора источника данных (CSV или папка).
        Создаёт новый итератор и показывает первое изображение.
        """
  
        folder_path = QFileDialog.getExistingDirectory(
            self, "Выберите папку с изображениями"
        )
        source_path = folder_path


        if not source_path:
            source_path, _ = QFileDialog.getOpenFileName(
                self,
                "Выберите CSV-аннотацию",
                "",
                "CSV Files (*.csv);;All Files (*)"
            )
            if not source_path:
                return 

        try:
            self.iterator = ImageIterator(source_path)
            self.iterator.index = 0  

            total = len(self.iterator)
            self.status_bar.showMessage(f"Загружено изображений: {total} — {os.path.basename(source_path)}")

            self.btn_prev.setEnabled(False)
            self.btn_next.setEnabled(total > 0)

            if total > 0:
                self.show_next()
            else:
                QMessageBox.information(self, "Пустой датасет", "В выбранном источнике нет изображений.")
                self.image_label.setText("Нет изображений для отображения")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка загрузки", f"Не удалось загрузить датасет:\n\n{e}")
            self.iterator = None

    def display_image(self, image_path: str) -> None:
        """
        Отображает изображение по указанному пути с масштабированием под размер окна.

        Args:
            image_path: Абсолютный путь к изображению.
        """
        if not os.path.exists(image_path):
            self.image_label.setText(f"Файл не найден:\n{image_path}")
            return

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self.image_label.setText("Не удалось загрузить изображение\n(неподдерживаемый формат?)")
            return

        scaled_pixmap = pixmap.scaled(
            self.image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
        self.current_path = image_path

        if self.iterator:
            current_idx = self.iterator.index
            total = len(self.iterator)
            filename = os.path.basename(image_path)
            self.status_bar.showMessage(f"{filename}  •  {current_idx}/{total}  •  {image_path}")

    def show_next(self) -> None:
        """Переходит к следующему изображению в датасете."""
        if not self.iterator:
            return

        try:
            path = next(self.iterator)
            self.display_image(path)
            self.btn_prev.setEnabled(True)
        except StopIteration:
            self.btn_next.setEnabled(False)
            QMessageBox.information(self, "Конец датасета", "Это было последнее изображение.")

    def show_previous(self) -> None:
        """Возвращается к предыдущему изображению."""
        if not self.iterator or self.iterator.index <= 1:
            self.btn_prev.setEnabled(False)
            return

    
        self.iterator.index -= 2
        if self.iterator.index < 0:
            self.iterator.index = 0

        try:
            path = next(self.iterator)
            self.display_image(path)
            self.btn_next.setEnabled(True)
        except StopIteration:
            pass

    def resizeEvent(self, event) -> None:
        """
        Перехватывает изменение размера окна и перерисовывает текущее изображение.

        Args:
            event: Событие изменения размера.
        """
        if self.current_path:
            self.display_image(self.current_path)
        super().resizeEvent(event)


def main() -> None:
    """Точка входа в приложение."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion") 

    window = DatasetViewer()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()