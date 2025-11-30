import os
import sys

from file_iterator import FileIterator

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QPixmap, QResizeEvent
from PyQt5.QtWidgets import (
    QApplication, QFileDialog, QHBoxLayout, QLabel, QMainWindow,
    QMessageBox, QPushButton, QVBoxLayout, QWidget)


window_width = 800
window_heights = 650


class MainWindow(QMainWindow):
    """
    Главное окно приложения для просмотра датасета изображений.
    """

    def __init__(self: QMainWindow) -> None:
        """
        Инициализация главного окна и внутренних переменных
        """
        super().__init__()
        self.setWindowTitle("Просмотр датасета изображений (Вариант 6)")
        self.setGeometry(100, 100, window_width, window_heights)

        self.iterator = None
        self.current_pixmap = None

        self._setup_ui()
        self.next_button.setEnabled(False)

    def _setup_ui(self: QMainWindow) -> None:
        """
        Создает и компонует виджеты интерфейса
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        self.image_label = QLabel("Выберите файл аннотации")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid #ccc; background-color: #f0f0f0;")

        self.image_label.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored,
            QtWidgets.QSizePolicy.Ignored)

        main_layout.addWidget(self.image_label)

        control_layout = QHBoxLayout()

        self.select_file_button = QPushButton("Выбрать аннотацию (CSV)")
        self.select_file_button.clicked.connect(self.select_annotation_file)
        control_layout.addWidget(self.select_file_button)

        self.next_button = QPushButton("Следующее изображение")
        self.next_button.clicked.connect(self.load_next_image)
        control_layout.addWidget(self.next_button)

        main_layout.addLayout(control_layout)

        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ожидание выбора файла.")

        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)

        self.next_button = QPushButton()
        self.select_file_button = QPushButton()
        self.status_bar = self.statusBar()
        

    def select_annotation_file(self: QWidget) -> None:
        """
        Открывает QFileDialog для выбора файла и инициализирует итератор
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл аннотации",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )

        if file_path:
            try:
                self.iterator = FileIterator(file_path)
                self.load_next_image()

                self.next_button.setEnabled(True)
                self.select_file_button.setText("Сменить аннотацию")

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Ошибка Инициализации",
                    f"Не удалось инициализировать итератор: {e}"
                )
                self.status_bar.showMessage("Ошибка: Итератор не инициализирован.")
                self.iterator = None
                self.next_button.setEnabled(False)

    def load_next_image(self: QWidget) -> None:
        """
        Получает следующий путь из итератора и отображает изображение
        """
        if not self.iterator:
            self.status_bar.showMessage("Ошибка: Итератор не активен.")
            return

        try:
            line = next(self.iterator).strip()

            if ',' in line:
                image_path = line.split(',')[0].strip()
            else:
                image_path = line.strip()

            self._display_image(image_path)
            self.status_bar.showMessage(
                f"Загружен файл: {os.path.basename(image_path)}"
            )

        except StopIteration:
            self.status_bar.showMessage("Конец датасета. Файлы закончились.")
            self.next_button.setEnabled(False)
            self.image_label.setText("Датасет просмотрен.")
            self.current_pixmap = None
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при загрузке данных: {e}")

    def _display_image(self, path: str) -> None:
        pass

    def _scale_and_set_pixmap(self) -> None:
        pass

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)


def main()-> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()