import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from iterator import DatasetIterator


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dataset Viewer")
        self.setGeometry(200, 200, 800, 600)

        self.iterator = None


        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(layout)


        btn_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(btn_layout)

        self.btn_select_folder = QtWidgets.QPushButton("Выбрать папку датасета")
        self.btn_select_folder.clicked.connect(self.select_dataset_folder)
        btn_layout.addWidget(self.btn_select_folder)

        self.btn_select_file = QtWidgets.QPushButton("Выбрать файл аннотаций")
        self.btn_select_file.clicked.connect(self.select_annotation_file)
        btn_layout.addWidget(self.btn_select_file)


        self.image_label = QtWidgets.QLabel()
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.image_label)

        nav_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(nav_layout)

        self.btn_prev = QtWidgets.QPushButton("Предыдущее изображение")
        self.btn_prev.clicked.connect(self.show_prev_image)
        self.btn_prev.setEnabled(False)
        nav_layout.addWidget(self.btn_prev)

        self.btn_next = QtWidgets.QPushButton("Следующее изображение")
        self.btn_next.clicked.connect(self.show_next_image)
        self.btn_next.setEnabled(False)
        nav_layout.addWidget(self.btn_next)


    def select_dataset_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder:
            try:
                self.iterator = DatasetIterator(dataset_path=folder)
                self.btn_prev.setEnabled(True)
                self.btn_next.setEnabled(True)
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))


    def select_annotation_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл аннотаций", filter="CSV Files (*.csv)")
        if file_path:
            try:
                self.iterator = DatasetIterator(annotation_file=file_path)
                self.btn_prev.setEnabled(True)
                self.btn_next.setEnabled(True)
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def show_prev_image(self):
        if self.iterator is None:
            return

        try:
            item = self.iterator.prev()
            abs_path = item[0]

            pixmap = QtGui.QPixmap(abs_path)
            if pixmap.isNull():
                raise ValueError("Невозможно загрузить изображение")

            scaled = pixmap.scaled(
                self.image_label.width(),
                self.image_label.height(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)

        except IndexError:
            QtWidgets.QMessageBox.information(self, "Старт", "Это первое изображение.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def show_next_image(self):
        if self.iterator is None:
            return

        try:
            item = next(self.iterator)
            abs_path = item[0]

            if not os.path.exists(abs_path):
                raise FileNotFoundError(f"Файл не найден: {abs_path}")

            pixmap = QtGui.QPixmap(abs_path)
            if pixmap.isNull():
                raise ValueError("Невозможно загрузить изображение")

            # масштабируем изображение с сохранением пропорций
            scaled = pixmap.scaled(
                self.image_label.width(),
                self.image_label.height(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)

        except StopIteration:
            QtWidgets.QMessageBox.information(self, "Конец", "Датасет завершён.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
