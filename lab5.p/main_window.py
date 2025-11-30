"""
Лабораторная работа №5:
Графическое приложение для просмотра изображений из датасета.
Использует PathIterator из лабораторной №2 (lab2.py).
"""

import os
import PyQt5

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(
    os.path.dirname(PyQt5.__file__),
    "Qt",
    "plugins",
    "platforms",
)
import sys
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QGraphicsScene,
    QGraphicsPixmapItem,
)

from win import Ui_MainWindow
from lab2 import PathIterator


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Главное окно приложения.
    Позволяет выбирать CSV/папку и листать изображения через PathIterator.
    """

    def __init__(self, parent: Optional[QMainWindow] = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.iterator: Optional[PathIterator] = None
        self.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)

        self.pushButton_2.clicked.connect(self.open_source)
        self.pushButton.clicked.connect(self.next_image)

    def open_source(self) -> None:
        """
        Выбор файла CSV или директории датасета
        и создание PathIterator.
        """
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите CSV или папку датасета",
            "",
            "CSV файлы (*.csv);;Все файлы (*.*)",
        )

        if not path:
            return

        try:
            self.iterator = PathIterator(path)
            self.label.setText(f"Источник: {path}")
            self.next_image()
        except Exception as exc:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать итератор:\n{exc}")
            self.iterator = None

    def next_image(self) -> None:
        """
        Отображает следующее изображение из итератора
        с сохранением пропорций.
        """
        if self.iterator is None:
            QMessageBox.information(
                self,
                "Нет данных",
                "Сначала откройте файл аннотации или папку датасета.",
            )
            return

        try:
            abs_path, rel_path = next(self.iterator)
        except StopIteration:
            self.iterator = iter(self.iterator)
            abs_path, rel_path = next(self.iterator)
        except Exception as exc:
            QMessageBox.critical(self, "Ошибка", f"Итератор завершился:\n{exc}")
            return

        pix = QPixmap(abs_path)
        if pix.isNull():
            QMessageBox.warning(
                self, "Ошибка", f"Не удалось открыть изображение:\n{abs_path}"
            )
            return

        target_size = self.graphicsView.viewport().size()
        scaled = pix.scaled(
            target_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        self.scene.clear()
        self.scene.addItem(QGraphicsPixmapItem(scaled))
        self.label.setText(f"Файл: {abs_path}")


def main() -> None:
    """
    Точка входа.
    """
    app = QApplication(sys.argv)
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
