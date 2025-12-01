import os
import PyQt5

qt_plugins_root = os.path.join(os.path.dirname(PyQt5.__file__), "Qt5", "plugins")

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(qt_plugins_root, "platforms")

os.environ["QT_PLUGIN_PATH"] = qt_plugins_root

os.environ["QT_IMAGEFORMAT_PLUGIN_PATH"] = os.path.join(qt_plugins_root, "imageformats")

import sys
from pathlib import Path
from typing import Optional, Iterator

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from lab2_var5 import PathIterator

class MainWindow(QMainWindow):
    """
    Главное окно приложения для просмотра изображений из датасета (хранение виджетов интерфейса, итератор путей и текущее изображение)
    """
    def __init__(self) -> None:
        """
        Инициализация главного окна, создание виджетов и подключение сигналов
        """
        super().__init__()
        self.setWindowTitle("Просмотр датасета изображений")

        # Итератор по путям и текущее изображение
        self.path_iterator: Optional[PathIterator] = None
        self.current_pixmap: Optional[Iterator[Path]] = None

        # Создание интерфейса
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.image_label = QLabel("Здесь будет изображение", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(320, 240)

        self.btn_open_folder = QPushButton("Выбрать папку датасета", self)
        self.btn_open_csv = QPushButton("Выбрать CSV-аннотацию", self)
        self.btn_next = QPushButton("Следующее изображение", self)
        self.btn_next.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.btn_open_folder)
        layout.addWidget(self.btn_open_csv)
        layout.addWidget(self.btn_next)

        central_widget.setLayout(layout)

        # Подключение сигналов к слотам
        self.btn_open_folder.clicked.connect(self.on_choose_folder)
        self.btn_open_csv.clicked.connect(self.on_choose_csv)
        self.btn_next.clicked.connect(self.on_next_image)

        # Статус-бар
        self.statusBar().showMessage("Выберите папку или CSV с путями к изображениям.")

    def on_choose_folder(self) -> None:
        """
        Обработка выбора папки с изображениями и создание итератора по этой папке
        """
        folder_path = QFileDialog.getExistingDirectory(self,"Выбор папки с изображениями","")
        if not folder_path:
            return

        self.path_iterator = PathIterator(folder_path=Path(folder_path))
        self.paths_iter = iter(self.path_iterator)
        self.statusBar().showMessage(f"Выбрана папка: {folder_path}")
        self.btn_next.setEnabled(True)
        self.show_next_image()

    def on_choose_csv(self) -> None:
        """
        Обработка выбора CSV-файла аннотации и создание итератора по этому файлу
        """
        csv_path, _ = QFileDialog.getOpenFileName(self,"Выбор CSV-аннотации","","CSV files (*.csv);;All files (*)")
        if not csv_path:
            return

        self.path_iterator = PathIterator(csv_path=Path(csv_path))
        self.paths_iter = iter(self.path_iterator)
        self.statusBar().showMessage(f"Выбран CSV-файл: {csv_path}")
        self.btn_next.setEnabled(True)
        self.show_next_image()

    def on_next_image(self) -> None:
        """
        Обработка нажатия кнопки «Следующее изображение»
        """
        self.show_next_image()

    def show_next_image(self) -> None:
        """
        Показ следующего изображения из PathIterator
        """
        if self.path_iterator is None:
            self.show_warning("Сначала выберите папку или CSV с датасетом.")
            return

        # если ещё не создали итератор – создаём
        if self.paths_iter is None:
            self.paths_iter = iter(self.path_iterator)

        try:
            next_path = next(self.paths_iter)
        except StopIteration:
            self.show_warning("Изображения закончились.")
            # можно сбросить на начало:
            # self.paths_iter = iter(self.path_iterator)
            return

        image_path = Path(next_path)
        if not image_path.is_file():
            self.show_warning(f"Файл не найден: {image_path}")
            return

        pixmap = QPixmap(str(image_path))
        if pixmap.isNull():
            self.show_warning(f"Не удалось загрузить изображение: {image_path}")
            return

        self.current_pixmap = pixmap
        self.update_image_label()
        self.statusBar().showMessage(str(image_path))

    def update_image_label(self) -> None:
        """
        Масштабирование текущего QPixmap под размер QLabel с сохранением пропорций и установка его на метку
        """
        if self.current_pixmap is None:
            return

        target_size = self.image_label.size()
        scaled = self.current_pixmap.scaled(
            target_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.image_label.setPixmap(scaled)

    def show_warning(self, text: str) -> None:
        """
        Показ окна предупреждения с указанным текстом
        """
        QMessageBox.warning(self, "Предупреждение", text)

    def resizeEvent(self, event) -> None:  # type: ignore[override]
        """
        Обработка изменения размера окна и пересчет размера изображения
        """
        super().resizeEvent(event)
        self.update_image_label()

def create_application() -> QApplication:
    """
    Создание и возвращение экземпляра QApplication
    """
    app = QApplication(sys.argv)
    return app


def create_main_window() -> MainWindow:
    """
    Создание и возвращение главного окна приложения
    """
    window = MainWindow()
    return window


def run_application(app: QApplication, window: MainWindow) -> None:
    """
    Показ главного окна и запуск главного цикла приложения
    """
    window.show()
    app.exec_()

def main() -> None:
    """
    Главная функция
    """
    app = create_application()
    window = create_main_window()
    run_application(app, window)


if __name__ == "__main__":
    main()