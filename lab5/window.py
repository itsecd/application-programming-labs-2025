import sys
import os
from typing import Optional
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from iterator import AnnotationIterator


class MainWindow(QtWidgets.QMainWindow):
    """
    Главное окно приложения для просмотра датасета
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Dataset Viewer (ЛР5)")
        self.resize(900, 650)

        self.iterator: Optional[AnnotationIterator] = None
        self.index: int = 0

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        btn_folder = QtWidgets.QPushButton("Выбрать папку датасета")
        btn_folder.clicked.connect(self.select_folder)
        layout.addWidget(btn_folder)

        self.image_label = QtWidgets.QLabel("Выберите папку с датасетом")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid gray;")
        layout.addWidget(self.image_label)

        nav_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(nav_layout)

        self.btn_prev = QtWidgets.QPushButton("Предыдущее")
        self.btn_prev.clicked.connect(self.show_prev)
        self.btn_prev.setEnabled(False)
        nav_layout.addWidget(self.btn_prev)

        self.btn_next = QtWidgets.QPushButton("Следующее")
        self.btn_next.clicked.connect(self.show_next)
        self.btn_next.setEnabled(False)
        nav_layout.addWidget(self.btn_next)


    def select_folder(self) -> None:
        """
        Выбор папки и загрузка CSV-аннотации
        """
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        if not path:
            return

        csvs = [f for f in os.listdir(path) if f.endswith(".csv")]
        if not csvs:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "В папке не найден CSV.")
            return

        csv_path = os.path.join(path, csvs[0])

        try:
            self.iterator = AnnotationIterator(csv_path)
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(exc))
            return

        self.index = 0
        self.btn_next.setEnabled(True)
        self.btn_prev.setEnabled(True)
        self.show_image()


    def show_image(self) -> None:
        """
        Отображение изображения по текущему индексу
        """
        if not self.iterator:
            return

        try:
            img_path = self.iterator.data[self.index]
        except IndexError:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Некорректный индекс.")
            return

        pixmap = QtGui.QPixmap(img_path)

        if pixmap.isNull():
            self.image_label.setText(f"Ошибка загрузки: {img_path}")
            return

        pixmap = pixmap.scaled(
            self.image_label.width(),
            self.image_label.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.image_label.setPixmap(pixmap)


    def show_next(self) -> None:
        """
        Показать следующее изображение
        """
        if not self.iterator:
            return

        if self.index + 1 >= len(self.iterator.data):
            QtWidgets.QMessageBox.information(self, "Конец", "Изображения закончились ^^")
            return

        self.index += 1
        self.show_image()


    def show_prev(self) -> None:
        """
        Показать предыдущее изображение
        """
        if not self.iterator:
            return

        if self.index <= 0:
            QtWidgets.QMessageBox.information(self, "Начало", "Первое изображение.")
            return

        self.index -= 1
        self.show_image()


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
