"""
Лабораторная работа №5.
Графическое приложение для просмотра изображений из датасета.

- Использует PathIterator из лабораторной №2 (lab2.py).
- Умеет работать как с CSV-аннотацией, так и с папкой датасета.
"""

import os
import sys
from pathlib import Path
from typing import Optional

import PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QFileDialog,
    QMainWindow,
    QMessageBox,
)

from lab2 import PathIterator
from win import Ui_MainWindow


# Хак для Qt, чтобы он находил плагин "windows" (qwindows.dll)
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(
    os.path.dirname(PyQt5.__file__),
    "Qt",
    "plugins",
    "platforms",
)


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Главное окно приложения.

    Позволяет:
    - выбрать CSV-файл аннотации ИЛИ папку с изображениями (через выбор любого файла);
    - листать изображения из датасета с помощью PathIterator;
    - отображать изображения с сохранением пропорций.
    """

    def __init__(self, parent: Optional[QMainWindow] = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.iterator: Optional[PathIterator] = None

        # Сцена для вывода изображений
        self.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)

        # Кнопки
        self.pushButton_2.clicked.connect(self.open_source)  # "Открыть"
        self.pushButton.clicked.connect(self.next_image)  # "Следущее"

    def open_source(self) -> None:
        """
        Открывает диалог выбора файла:
        - если выбран .csv → используем его как аннотацию;
        - иначе считаем, что пользователь выбрал картинку → берём её директорию
          как корень датасета.
        Создаём PathIterator по полученному источнику.
        """
        path_str, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите CSV-файл или любую картинку из папки датасета",
            "",
            "CSV файлы (*.csv);;Изображения (*.jpg *.jpeg *.png *.bmp *.gif *.webp);;Все файлы (*.*)",
        )

        if not path_str:
            return

        p = Path(path_str)

        # Определяем, что именно выбрали
        if p.is_file() and p.suffix.lower() == ".csv":
            source = str(p)  # Аннотация CSV
        else:
            source = str(p.parent)  # Папка, где лежит выбранное изображение

        try:
            self.iterator = PathIterator(source)
            # Сбрасываем итератор на начало
            self.iterator = iter(self.iterator)
            self.label.setText(f"Источник: {source}")
            # Сразу показываем первое изображение
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
                "Сначала откройте CSV-файл или папку датасета.",
            )
            return

        # Пытаемся получить следующую пару путей [abs, rel]
        try:
            abs_path, rel_path = next(self.iterator)
        except StopIteration:
            # Дошли до конца — начинаем сначала
            self.iterator = iter(self.iterator)
            abs_path, rel_path = next(self.iterator)
        except Exception as exc:
            QMessageBox.critical(self, "Ошибка", f"Ошибка итератора:\n{exc}")
            return

        pixmap = QPixmap(abs_path)
        if pixmap.isNull():
            QMessageBox.warning(
                self,
                "Ошибка",
                f"Не удалось открыть изображение:\n{abs_path}",
            )
            return

        # Масштабируем под размер окна, сохраняя пропорции
        target_size = self.graphicsView.viewport().size()
        scaled = pixmap.scaled(
            target_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        # Очищаем сцену и добавляем новое изображение
        self.scene.clear()
        self.scene.addItem(QGraphicsPixmapItem(scaled))

        # Обновляем подпись с путём к файлу
        self.label.setText(f"Файл: {abs_path}")


def main() -> None:
    """
    Точка входа в приложение.
    Создаёт QApplication, окно и запускает цикл обработки событий.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
