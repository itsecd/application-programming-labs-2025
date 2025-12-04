import os
import sys
from typing import Optional

from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                           QHBoxLayout, QWidget, QPushButton, QLabel,
                           QFileDialog, QMessageBox, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from dataset_iterator import DatasetIterator


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        """Инициализация главного окна."""
        super().__init__()
        self.dataset_iterator: Optional[DatasetIterator] = None
        self.current_image_path: Optional[str] = None
        
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Настройка пользовательского интерфейса."""
        self.setWindowTitle("Просмотр датасета изображений")
        self.setMinimumSize(1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)

        self._create_source_buttons(layout)
        self._create_image_display(layout)
        self._create_navigation(layout)
        self._create_status(layout)

    def _create_source_buttons(self, layout: QVBoxLayout) -> None:
        """Создает кнопки выбора источника данных."""
        button_layout = QHBoxLayout()

        self.btn_folder = QPushButton("Выбрать папку")
        self.btn_folder.clicked.connect(self._select_folder)

        self.btn_annotation = QPushButton("Выбрать аннотацию")
        self.btn_annotation.clicked.connect(self._select_annotation)

        button_layout.addWidget(self.btn_folder)
        button_layout.addWidget(self.btn_annotation)
        button_layout.addStretch()

        layout.addLayout(button_layout)

    def _create_image_display(self, layout: QVBoxLayout) -> None:
        """Создает область для отображения изображения."""
        self.image_frame = QFrame()
        self.image_frame.setFrameStyle(QFrame.Shape.Box)
        self.image_frame.setMinimumSize(600, 400)

        frame_layout = QVBoxLayout(self.image_frame)
        frame_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.image_label = QLabel("Выберите источник данных")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(500, 350)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, 
                                     QSizePolicy.Policy.Expanding)

        frame_layout.addWidget(self.image_label)
        layout.addWidget(self.image_frame, 1)

    def _create_navigation(self, layout: QVBoxLayout) -> None:
        """Создает панель навигации."""
        nav_layout = QHBoxLayout()

        self.btn_prev = QPushButton("Назад")
        self.btn_prev.clicked.connect(self._show_previous)
        self.btn_prev.setEnabled(False)

        self.counter_label = QLabel("0 / 0")
        self.counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_next = QPushButton("Вперед")
        self.btn_next.clicked.connect(self._show_next)
        self.btn_next.setEnabled(False)

        nav_layout.addWidget(self.btn_prev)
        nav_layout.addWidget(self.counter_label)
        nav_layout.addWidget(self.btn_next)

        layout.addLayout(nav_layout)

    def _create_status(self, layout: QVBoxLayout) -> None:
        """Создает статусную строку."""
        self.status_label = QLabel("Готов к работе")
        layout.addWidget(self.status_label)

    def _select_folder(self) -> None:
        """Обрабатывает выбор папки."""
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder:
            try:
                print(f"\nЗагрузка из папки: {folder}")
                self.dataset_iterator = DatasetIterator(folder_path=folder)
                print(f"Успешно загружено из папки: {len(self.dataset_iterator)} изображений")
                self._initialize_viewer()
            except Exception as e:
                print(f"Ошибка загрузки папки: {e}")
                self._show_error(f"Ошибка загрузки папки: {e}")

    def _select_annotation(self) -> None:
        """Обрабатывает выбор файла аннотации."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл аннотации", "", "CSV (*.csv)"
        )
        if file_path:
            try:
                print(f"\nЗагрузка аннотации: {file_path}")
                self.dataset_iterator = DatasetIterator(annotation_file=file_path)
                print(f"Успешно загружено из аннотации: {len(self.dataset_iterator)} изображений")
                self._initialize_viewer()
            except Exception as e:
                print(f"Ошибка загрузки аннотации: {e}")
                self._show_error(f"Ошибка загрузки аннотации: {e}")

    def _initialize_viewer(self) -> None:
        """Инициализирует просмотрщик после загрузки данных."""
        if self.dataset_iterator and len(self.dataset_iterator) > 0:
            self.btn_next.setEnabled(True)
            self.btn_prev.setEnabled(True)
            count = len(self.dataset_iterator)
            self.status_label.setText(f"Загружено: {count} изображений")
            self._show_next()
        else:
            error_msg = "Нет изображений для отображения"
            print(error_msg)
            self._show_error(error_msg)

    def _show_next(self) -> None:
        """Показывает следующее изображение."""
        if self.dataset_iterator and self.dataset_iterator.has_next():
            try:
                image_path = next(self.dataset_iterator)
                print(f"Отображение изображения: {os.path.basename(image_path)}")
                self._display_image(image_path)
            except Exception as e:
                print(f"Ошибка загрузки изображения: {e}")
                self._show_error(f"Ошибка загрузки изображения: {e}")

    def _show_previous(self) -> None:
        """Показывает предыдущее изображение."""
        if self.dataset_iterator and self.dataset_iterator.has_previous():
            try:
                prev_image = self.dataset_iterator.get_previous_image()
                if prev_image:
                    current_idx = self.dataset_iterator.get_current_index()
                    self.dataset_iterator.reset()
                    for _ in range(current_idx - 2):
                        next(self.dataset_iterator)
                    print(f"Отображение предыдущего изображения: {os.path.basename(prev_image)}")
                    self._display_image(prev_image)
            except Exception as e:
                print(f"Ошибка навигации: {e}")
                self._show_error(f"Ошибка навигации: {e}")

    def _display_image(self, image_path: str) -> None:
        """Отображает изображение с сохранением пропорций."""
        try:
            self.current_image_path = image_path
            pixmap = QPixmap(image_path)

            if pixmap.isNull():
                error_text = "Ошибка загрузки изображения"
                print(error_text)
                self.image_label.setText(error_text)
                return

            label_size = self.image_label.size()
            scaled_pixmap = pixmap.scaled(
                label_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            self.image_label.setPixmap(scaled_pixmap)

            current_idx = self.dataset_iterator.get_current_index()
            total_count = len(self.dataset_iterator)
            filename = os.path.basename(image_path)

            self.counter_label.setText(f"{current_idx} / {total_count}")
            self.status_label.setText(f"Файл: {filename}")

            self.btn_prev.setEnabled(self.dataset_iterator.has_previous())
            self.btn_next.setEnabled(self.dataset_iterator.has_next())

        except Exception as e:
            print(f"Ошибка отображения: {e}")
            self._show_error(f"Ошибка отображения: {e}")

    def _show_error(self, message: str) -> None:
        """Показывает сообщение об ошибке."""
        QMessageBox.critical(self, "Ошибка", message)
        self.status_label.setText("Ошибка")

    def resizeEvent(self, event) -> None:
        """Обрабатывает изменение размера окна."""
        super().resizeEvent(event)
        if self.current_image_path:
            self._display_image(self.current_image_path)


def main():
    """Запускает приложение."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()