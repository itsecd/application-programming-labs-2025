import sys
import os
from typing import Optional

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox, QStatusBar
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from path_iterator import Path_Iterator


class MainWindow(QMainWindow):
    """
    Главное окно приложения для просмотра изображений из датасета.
    """
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Просмотр датасета")
        self.setGeometry(100, 100, 800, 600)

        self.iterator: Optional[Path_Iterator] = None

        self.init_ui()
        self.setup_status_bar()

        self.auto_load_pig_images()

    def init_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        btn_layout = QHBoxLayout()
        self.btn_folder = QPushButton("Выбрать другую папку")
        self.btn_csv = QPushButton("Выбрать annotation.csv")
        btn_layout.addWidget(self.btn_folder)
        btn_layout.addWidget(self.btn_csv)
        layout.addLayout(btn_layout)

        self.btn_next = QPushButton("Следующее")
        self.btn_next.setEnabled(False)
        layout.addWidget(self.btn_next)

        self.label = QLabel("Изображение появится здесь")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        layout.addWidget(self.label)

        central.setLayout(layout)

        self.btn_folder.clicked.connect(self.select_folder)
        self.btn_csv.clicked.connect(self.select_csv)
        self.btn_next.clicked.connect(self.show_next)

    def setup_status_bar(self) -> None:
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готово")

    def auto_load_pig_images(self) -> None:
        """
        Автоматически загружает папку 'pig_images', если она существует.
        """
        pig_dir = "pig_images"
        if os.path.exists(pig_dir) and os.path.isdir(pig_dir):
            self.load_dataset(pig_dir)
            self.status_bar.showMessage(f"Автоматически загружено: {pig_dir}")
        else:
            self.status_bar.showMessage("Папка 'pig_images' не найдена. Выберите источник вручную.")

    def load_dataset(self, path: str) -> None:
        """
        Инициализирует итератор и загружает первый элемент.
        """
        try:
            self.iterator = Path_Iterator(path)
            if not self.iterator.items:
                raise ValueError("Датасет пуст.")
            self.btn_next.setEnabled(True)
            self.status_bar.showMessage(f"Загружено {len(self.iterator.items)} элементов.")
            self.show_next()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные:\n{e}")
            self.btn_next.setEnabled(False)
            self.iterator = None

    def select_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с изображениями")
        if folder:
            self.load_dataset(folder)

    def select_csv(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите annotation.csv", "", "CSV файлы (*.csv);;Все файлы (*)"
        )
        if file_path:
            self.load_dataset(file_path)

    def show_next(self) -> None:
        if self.iterator is None:
            QMessageBox.warning(self, "Внимание", "Сначала загрузите данные.")
            return

        try:
            absolute_path, relative_path = next(self.iterator)
            if not os.path.exists(absolute_path):
                raise FileNotFoundError(f"Файл не найден: {absolute_path}")

            if absolute_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                pixmap = QPixmap(absolute_path)
                if pixmap.isNull():
                    raise ValueError("Не удалось загрузить изображение.")
                scaled = pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.label.setPixmap(scaled)
                self.status_bar.showMessage(f"Отображено: {os.path.basename(absolute_path)}")
            else:
                self.label.setText(f"Неподдерживаемый формат:\n{os.path.basename(absolute_path)}")
                self.status_bar.showMessage("Поддерживаются только изображения.")

        except StopIteration:
            QMessageBox.information(self, "Конец", "Больше изображений нет.")
            self.btn_next.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при отображении:\n{e}")
            self.btn_next.setEnabled(False)


def main() -> None:
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()