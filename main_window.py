import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from lab2_var12 import Iterator_csv


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Просмотр датасета")
        self.resize(800, 600)
        # цетральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        # кнопки
        self.button_load = QPushButton("Выберите файл анотации")
        self.button_next = QPushButton("Следующие изображение")
        self.button_next.setEnabled(False)
        # настройка изображения
        self.imeg_label = QLabel("Изображение отсуствует")
        self.imeg_label.setAlignment(Qt.AlignCenter)
        # настройка сигналов
        self.button_load.clicked.connect(self.load_annotation)
        self.button_next.clicked.connect(self.next_img)
        # добавление виджетов в макет
        layout.addWidget(self.button_load)
        layout.addWidget(self.button_next)
        layout.addWidget(self.imeg_label)

        self.iterator = None
        self.curent_item = None

    def load_annotation(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Выберите csv файл", "", "CSV Files(*.csv)"
            )
            if not file_path:
                return

            self.iterator = Iterator_csv(file_path)
            self.iterator.index = 0
            self.curent_item = next(self.iterator)
            self.show_img(self.curent_item)
            self.button_next.setEnabled(True)
        except Exception as e:
            print(f"[ERROR] Ошибка при загрузке аннотации: {e}", file=sys.stderr)
            QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось загрузить файл аннотации.",
            )

    def show_img(self, item):
        try:
            path = item.get("absolute_path")
            if not path:
                raise ValueError("В записи отсутствует поле 'absolute_path'")
            pixmar = QPixmap(path)
            if pixmar.isNull():
                raise RuntimeError(f"Не удалось загрузить изображение: {path}")
            scarled_pixmar = pixmar.scaled(
                800,
                600,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
            self.imeg_label.setPixmap(scarled_pixmar)
        except Exception as e:
            print(f"[ERROR] Ошибка при отображении изображения: {e}", file=sys.stderr)
            self.imeg_label.setText(f"Ошибка отображения изображения.")

    def next_img(self):
        if self.iterator is None:
            return

        try:
            self.curent_item = next(self.iterator)
            self.show_img(self.curent_item)
        except StopIteration:
            self.imeg_label.setText("Конец списка изображений,картинок больше не будет")
            self.button_next.setEnabled(False)
        except Exception as e:
            print(
                f"[ERROR] Ошибка при переходе к следующему изображению: {e}",
                file=sys.stderr,
            )
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Не удалось загрузить следующее изображение.",
            )
            self.button_next.setEnabled(False)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
