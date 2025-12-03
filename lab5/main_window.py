import cv2
import sys
import os
import numpy as np
from typing import Optional, Tuple

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QFileDialog,
    QMessageBox, QCheckBox, QTextEdit, QComboBox
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

try:
    from iterator_module import FileIterator
    from image_processor import ImageProcessor
except ImportError as e:
    print(f"Критическая ошибка: Не найдены необходимые модули. {e}")
    sys.exit(1)


class DatasetViewer(QMainWindow):
    """
    Главное окно приложения для просмотра, анализа и сохранения изображений.

    Интеграция:
    - FileIterator (обход CSV).
    - ImageProcessor (обрезка в круг, сохранение, инфо).
    - Аналитика (RGB диапазоны).
    """

    def __init__(self) -> None:
        """Инициализация главного окна и переменных состояния."""
        super().__init__()

        self.iterator: Optional[FileIterator] = None
        self.current_image_path: Optional[str] = None

        self.current_processor: Optional[ImageProcessor] = None

        self._init_ui()

    def _init_ui(self) -> None:
        """Настройка графического интерфейса пользователя (GUI)."""
        self.setWindowTitle("Dataset Viewer & Editor")
        self.resize(1100, 750)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        image_layout = QVBoxLayout()
        self.image_label = QLabel("Изображение не загружено")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet(
            "border: 2px dashed #cccccc; background-color: #f9f9f9;"
        )
        self.image_label.setMinimumSize(600, 500)
        image_layout.addWidget(self.image_label, stretch=1)
        main_layout.addLayout(image_layout, stretch=3)

        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(10)

        controls_layout.addWidget(QLabel("<b>1. Данные </b>"))
        self.btn_load_csv = QPushButton("📂 Загрузить annotation.csv")
        self.btn_load_csv.clicked.connect(self.load_annotation_file)
        controls_layout.addWidget(self.btn_load_csv)

        controls_layout.addWidget(QLabel("<b>2. Навигация</b>"))
        self.btn_next = QPushButton("Следующее изображение ➡")
        self.btn_next.setEnabled(False)
        self.btn_next.clicked.connect(self.show_next_image)
        controls_layout.addWidget(self.btn_next)

        controls_layout.addSpacing(10)
        controls_layout.addWidget(QLabel("<b>3. Обработка </b>"))

        self.chk_circular = QCheckBox("Режим: Круглое изображение")
        self.chk_circular.toggled.connect(self.refresh_current_image)
        controls_layout.addWidget(self.chk_circular)

        controls_layout.addWidget(QLabel("Цвет фона:"))
        self.combo_bg = QComboBox()
        self.combo_bg.addItems(["transparent", "white", "black"])
        self.combo_bg.setToolTip("Выберите цвет фона для круглой обрезки")
        self.combo_bg.currentTextChanged.connect(self.refresh_current_image)
        controls_layout.addWidget(self.combo_bg)

        self.btn_save = QPushButton("💾 Сохранить текущее")
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self.save_current_image)
        controls_layout.addWidget(self.btn_save)

        controls_layout.addSpacing(10)
        controls_layout.addWidget(QLabel("<b>4. Информация и Аналитика</b>"))

        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setPlaceholderText("Здесь будет информация о файле и RGB каналах...")
        controls_layout.addWidget(self.info_text)

        controls_layout.addStretch()
        main_layout.addLayout(controls_layout, stretch=1)

    def load_annotation_file(self) -> None:
        """Открывает диалог выбора файла и инициализирует итератор."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите CSV", os.getcwd(), "CSV Files (*.csv);;All Files (*)"
        )

        if not file_path:
            return

        try:
            self.iterator = FileIterator(file_path)
            self.current_image_path = None
            self.current_processor = None

            self.image_label.setText("Готово. Нажмите 'Следующее'.")
            self.info_text.clear()
            self.btn_next.setEnabled(True)
            self.btn_save.setEnabled(False)

            QMessageBox.information(self, "Успех", f"Загружено строк: {len(self.iterator.paths)}")

        except Exception as e:
            self._show_error("Ошибка итератора", e)

    def show_next_image(self) -> None:
        """Получает следующий путь из итератора и обновляет GUI."""
        if self.iterator is None:
            return

        try:
            next_path = next(self.iterator)
            self.current_image_path = next_path

            self.current_processor = ImageProcessor(next_path)

            self.refresh_current_image()
            self._update_file_info()
            self.btn_save.setEnabled(True)

        except StopIteration:
            QMessageBox.information(self, "Конец", "Датасет пройден.")
            self.btn_next.setEnabled(False)
            self.btn_save.setEnabled(False)
        except Exception as e:
            self._show_error("Ошибка загрузки изображения", e)

    def refresh_current_image(self) -> None:
        """Обновляет отображение в зависимости от чекбокса и выбранного цвета."""
        if not self.current_processor:
            return

        try:
            if self.chk_circular.isChecked():
                bg_color = self.combo_bg.currentText()
                image_data = self.current_processor.make_circular(bg_color=bg_color)
            else:
                image_data = self.current_processor.original_image

            pixmap = self._convert_cv_to_pixmap(image_data)
            self._display_pixmap(pixmap)

        except Exception as e:
            self.image_label.setText("Ошибка обработки")
            print(f"Display error: {e}")

    def save_current_image(self) -> None:
        """Сохраняет текущее (обработанное или оригинал) изображение."""
        if not self.current_processor:
            return

        default_name = "processed_image.png"
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить изображение", default_name,
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if not save_path:
            return

        try:
            if self.chk_circular.isChecked():
                bg_color = self.combo_bg.currentText()
                img_to_save = self.current_processor.make_circular(bg_color=bg_color)
            else:
                img_to_save = self.current_processor.original_image

            self.current_processor.save_result_image(save_path, img_to_save)
            QMessageBox.information(self, "Сохранено", f"Файл сохранен:\n{save_path}")

        except Exception as e:
            self._show_error("Ошибка сохранения", e)

    def _update_file_info(self) -> None:
        """
        Выводит размеры и статистику (разность яркости) по каналам RGB.
        Статистика считается по ОРИГИНАЛЬНОМУ изображению.
        """
        if not self.current_processor:
            return

        try:
            base_info = self.current_processor.get_image_size_info().replace("\n", "<br>")

            img = self.current_processor.original_image

            if img is None:
                raise ValueError("Изображение пустое")

            b_ch, g_ch, r_ch = cv2.split(img)

            r_diff = int(np.max(r_ch)) - int(np.min(r_ch))
            g_diff = int(np.max(g_ch)) - int(np.min(g_ch))
            b_diff = int(np.max(b_ch)) - int(np.min(b_ch))

            stats_html = (
                f"<hr><b>RGB Статистика (Max - Min):</b><br>"
                f"<span style='color:red'>Red Diff: {r_diff}</span><br>"
                f"<span style='color:green'>Green Diff: {g_diff}</span><br>"
                f"<span style='color:blue'>Blue Diff: {b_diff}</span>"
            )

            full_html = f"{base_info}<br>{stats_html}"
            self.info_text.setHtml(full_html)

        except Exception as e:
            self.info_text.setText(f"Ошибка анализа данных: {e}")

    @staticmethod
    def _convert_cv_to_pixmap(cv_img: np.ndarray) -> QPixmap:
        """Конвертирует OpenCV изображение в QPixmap."""
        height, width = cv_img.shape[:2]

        if len(cv_img.shape) == 2:
            channels = 1
        else:
            channels = cv_img.shape[2]

        bytes_per_line = channels * width

        if channels == 4:
            q_img = QImage(
                cv_img.data, width, height, bytes_per_line,
                QImage.Format.Format_RGBA8888
            ).rgbSwapped()
        elif channels == 3:
            q_img = QImage(
                cv_img.data, width, height, bytes_per_line,
                QImage.Format.Format_RGB888
            ).rgbSwapped()
        else:
            q_img = QImage(
                cv_img.data, width, height, bytes_per_line,
                QImage.Format.Format_Grayscale8
            )

        return QPixmap.fromImage(q_img)

    def _display_pixmap(self, pixmap: QPixmap) -> None:
        """Масштабирует и показывает pixmap."""
        if pixmap.isNull():
            return

        w = self.image_label.width()
        h = self.image_label.height()

        scaled = pixmap.scaled(
            w, h,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled)

    def _show_error(self, title: str, error: Exception) -> None:
        """Показывает окно ошибки."""
        QMessageBox.critical(self, title, f"{str(error)}")

    def resizeEvent(self, event) -> None:
        """Обновляет картинку при ресайзе окна."""
        if self.current_processor:
            self.refresh_current_image()
        super().resizeEvent(event)


def main() -> None:
    app = QApplication(sys.argv)
    window = DatasetViewer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()