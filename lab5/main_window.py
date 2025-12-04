"""
Главное окно приложения для просмотра датасета изображений.

"""
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                           QHBoxLayout, QWidget, QPushButton, QLabel,
                           QFileDialog, QMessageBox, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from dataset_iterator import DatasetIterator


class MainWindow(QMainWindow):
    """Главное окно приложения для просмотра датасета изображений.
    
    Атрибуты:
        dataset_iterator: Объект итератора для работы с датасетом изображений
        current_image_path: Путь к текущему отображаемому файлу изображения
    """

    def __init__(self) -> None:
        """Инициализирует главное окно приложения."""
        super().__init__()
        self.dataset_iterator = None
        self.current_image_path = None

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Инициализирует пользовательский интерфейс.
        Создает и размещает все виджеты окна:
        1. Кнопки выбора источника данных
        2. Область для отображения изображения
        3. Панель навигации между изображениями
        4. Статусную строку с информацией
        """
        self.setWindowTitle("Просмотр датасета изображений")
        self.setMinimumSize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)

        self._create_source_buttons(main_layout)
        self._create_image_display(main_layout)
        self._create_navigation(main_layout)
        self._create_status(main_layout)

    def _create_source_buttons(self, layout: QVBoxLayout) -> None:
        """Создает кнопки выбора источника данных.
        
        Args:
            layout: Layout, в который добавляются кнопки
        """
        button_layout = QHBoxLayout()

        self.btn_folder = QPushButton("Выбрать папку датасета")
        self.btn_folder.clicked.connect(self._select_folder)
        
        self.btn_annotation = QPushButton("Выбрать файл аннотации")
        self.btn_annotation.clicked.connect(self._select_annotation)

        button_layout.addWidget(self.btn_folder)
        button_layout.addWidget(self.btn_annotation)
        button_layout.addStretch()

        layout.addLayout(button_layout)

    def _create_image_display(self, layout: QVBoxLayout) -> None:
        """Создает область для отображения изображения.
        
        Args:
            layout: Layout, в который добавляется область отображения
        """
        self.image_frame = QFrame()
        self.image_frame.setFrameStyle(QFrame.Box)
        self.image_frame.setMinimumSize(400, 300)
        self.image_frame.setStyleSheet("background-color: #f0f0f0;")

        frame_layout = QVBoxLayout(self.image_frame)
        frame_layout.setAlignment(Qt.AlignCenter)

        self.image_label = QLabel("Изображение будет отображено здесь")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(300, 200)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, 
                                     QSizePolicy.Expanding)

        frame_layout.addWidget(self.image_label)
        layout.addWidget(self.image_frame, 1)

    def _create_navigation(self, layout: QVBoxLayout) -> None:
        """Создает панель навигации между изображениями.
        
        Args:
            layout: Layout, в который добавляется панель навигации
        """
        nav_layout = QHBoxLayout()

        self.btn_prev = QPushButton("← Назад")
        self.btn_prev.clicked.connect(self._show_previous)
        self.btn_prev.setEnabled(False)

        self.counter_label = QLabel("0 / 0")
        self.counter_label.setAlignment(Qt.AlignCenter)

        self.btn_next = QPushButton("Вперед →")
        self.btn_next.clicked.connect(self._show_next)
        self.btn_next.setEnabled(False)

        nav_layout.addWidget(self.btn_prev)
        nav_layout.addWidget(self.counter_label, 1)
        nav_layout.addWidget(self.btn_next)

        layout.addLayout(nav_layout)

    def _create_status(self, layout: QVBoxLayout) -> None:
        """Создает статусную строку с информацией.
        
        Args:
            layout: Layout, в который добавляется статусная строка
        """
        self.status_label = QLabel("Выберите папку датасета или файл аннотации")
        self.status_label.setStyleSheet("font-weight: bold; padding: 5px;")
        layout.addWidget(self.status_label)

    def _select_folder(self) -> None:
        """Обрабатывает выбор папки с изображениями.
        
        Открывает диалоговое окно для выбора папки, создает итератор
        для работы с изображениями из выбранной папки.
        """
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Выберите папку с изображениями",
            os.path.expanduser("~")
        )
        
        if folder:
            try:
                self.dataset_iterator = DatasetIterator(folder_path=folder)
                
                if len(self.dataset_iterator) > 0:
                    self.btn_next.setEnabled(True)
                    self.btn_prev.setEnabled(True)
                    
                    self.status_label.setText(
                        f"Загружена папка: {os.path.basename(folder)} | "
                        f"Изображений: {len(self.dataset_iterator)}"
                    )
                    
                    self._show_next()
                else:
                    self._show_error("В выбранной папке нет изображений")
                    
            except Exception as e:
                self._show_error(f"Ошибка загрузки папки: {str(e)}")

    def _select_annotation(self) -> None:
        """Обрабатывает выбор файла аннотации.
        
        Открывает диалоговое окно для выбора CSV-файла, создает итератор
        для работы с путями из файла аннотации.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Выберите файл аннотации", 
            "", 
            "CSV файлы (*.csv);;Все файлы (*)"
        )
        
        if file_path:
            try:
                self.dataset_iterator = DatasetIterator(annotation_file=file_path)
                
                if len(self.dataset_iterator) > 0:
                    self.btn_next.setEnabled(True)
                    self.btn_prev.setEnabled(True)
                    
                    self.status_label.setText(
                        f"Загружен файл: {os.path.basename(file_path)} | "
                        f"Записей: {len(self.dataset_iterator)}"
                    )
                    
                    self._show_next()
                else:
                    self._show_error("В файле аннотации нет данных")
                    
            except Exception as e:
                self._show_error(f"Ошибка загрузки аннотации: {str(e)}")

    def _show_next(self) -> None:
        """Показывает следующее изображение из датасета.
        
        Получает следующий путь к файлу из итератора,
        обновляет информацию о файле и отображает изображение.
        """
        if self.dataset_iterator and self.dataset_iterator.has_next():
            try:
                image_path = next(self.dataset_iterator)
                self._display_image(image_path)
                
            except StopIteration:
                self.btn_next.setEnabled(False)
                self.status_label.setText("✓ Достигнут конец датасета")
                
            except Exception as e:
                self._show_error(f"Ошибка загрузки изображения: {str(e)}")

    def _show_previous(self) -> None:
        """Показывает предыдущее изображение из датасета.
        
        Перемещается к предыдущему изображению в коллекции.
        """
        if self.dataset_iterator and self.dataset_iterator.has_previous():
            try:
                current_idx = self.dataset_iterator.get_current_index()
                if current_idx > 2:
                    self.dataset_iterator.current_index = current_idx - 2
                    image_path = self.dataset_iterator.get_current_image()
                    self._display_image(image_path)
                    
            except Exception as e:
                self._show_error(f"Ошибка навигации: {str(e)}")

    def _display_image(self, image_path: str) -> None:
        """Отображает текущее изображение с сохранением пропорций.
        
        Args:
            image_path: Путь к файлу изображения
            
        Загружает изображение по указанному пути, масштабирует его
        с сохранением пропорций для отображения в метке.
        """
        try:
            self.current_image_path = image_path
            
            pixmap = QPixmap(image_path)

            if pixmap.isNull():
                self.image_label.setText("Не удалось загрузить изображение")
                return

            label_size = self.image_label.size()
            
            scaled_pixmap = pixmap.scaled(
                label_size.width() - 20,
                label_size.height() - 20,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
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
            self._show_error(f"Ошибка отображения: {str(e)}")

    def _show_error(self, message: str) -> None:
        """Показывает сообщение об ошибке.
        
        Args:
            message: Текст сообщения об ошибке
        """
        QMessageBox.critical(self, "Ошибка", message)
        self.image_label.setText("Ошибка загрузки")
        self.status_label.setText("Ошибка")

    def resizeEvent(self, event) -> None:
        """Обрабатывает событие изменения размера окна.
        
        Args:
            event: Событие изменения размера окна
            
        При изменении размера окна перерисовывает изображение,
        чтобы оно соответствовало новым размерам.
        """
        super().resizeEvent(event)
        if self.current_image_path and os.path.exists(self.current_image_path):
            self._display_image(self.current_image_path)


def main() -> None:
    """Точка входа в приложение.
    
    Создает экземпляр QApplication и главное окно приложения,
    запускает основной цикл обработки событий.
    """
    app = QApplication(sys.argv)
    
    try:
        from dataset_iterator import DatasetIterator
        print("Итератор успешно импортирован")
    except ImportError as e:
        print(f" Ошибка импорта итератора: {e}")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Ошибка импорта итератора")
        msg.setInformativeText("Убедитесь, что файл dataset_iterator.py находится в той же папке")
        msg.exec_()
        return
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()