import os
import sys

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from main import FilePathIterator


class MusicPlayer(QMainWindow):
    """Музыкальный плеер для просмотра датасета"""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Dataset Music Player")
        self.setGeometry(100, 100, 700, 500)

        self.file_iterator = None
        self.player = QMediaPlayer()
        self.current_file_path = None

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        source_layout = QHBoxLayout()

        source_label = QLabel("Источник данных:")
        source_layout.addWidget(source_label)

        self.folder_button = QPushButton("Выбрать папку")
        self.folder_button.clicked.connect(self.select_folder)
        source_layout.addWidget(self.folder_button)

        self.file_button = QPushButton("Выбрать CSV")
        self.file_button.clicked.connect(self.select_annotation_file)
        source_layout.addWidget(self.file_button)

        self.source_label_info = QLabel("Источник не выбран")
        self.source_label_info.setStyleSheet("color: gray; font-size: 10px;")
        source_layout.addWidget(self.source_label_info)
        source_layout.addStretch()

        main_layout.addLayout(source_layout)

        self.title_label = QLabel("Композиция не загружена")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)

        self.info_label = QLabel("")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-size: 11px; color: gray;")
        main_layout.addWidget(self.info_label)

        main_layout.addStretch()

        progress_layout = QHBoxLayout()

        self.time_label = QLabel("0:00")
        self.time_label.setMinimumWidth(50)
        self.time_label.setStyleSheet("font-weight: bold;")
        progress_layout.addWidget(self.time_label)

        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setMinimum(0)
        self.progress_slider.setMaximum(100)
        self.progress_slider.setValue(0)

        self.progress_slider.sliderMoved.connect(self.on_slider_moved)
        self.player.positionChanged.connect(self.on_position_changed)
        self.player.durationChanged.connect(self.on_duration_changed)

        progress_layout.addWidget(self.progress_slider)

        self.duration_label = QLabel("0:00")
        self.duration_label.setMinimumWidth(50)
        self.duration_label.setAlignment(Qt.AlignRight)
        self.duration_label.setStyleSheet("font-weight: bold;")
        progress_layout.addWidget(self.duration_label)

        main_layout.addLayout(progress_layout)

        main_layout.addStretch()

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.prev_button = QPushButton("← Предыдущая")
        self.prev_button.clicked.connect(self.show_previous)
        self.prev_button.setEnabled(False)
        button_layout.addWidget(self.prev_button)

        self.play_button = QPushButton("▶ Вперед")
        self.play_button.clicked.connect(self.show_next)
        self.play_button.setEnabled(False)
        button_layout.addWidget(self.play_button)

        self.pause_button = QPushButton("⏸ Пауза")
        self.pause_button.clicked.connect(self.toggle_pause)
        self.pause_button.setEnabled(False)
        button_layout.addWidget(self.pause_button)

        self.stop_button = QPushButton("⏹ Стоп")
        self.stop_button.clicked.connect(self.stop_playback)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)

        main_layout.addLayout(button_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.is_paused = False

    def select_folder(self) -> None:
        """Выбрать папку с музыкой"""
        folder_path = QFileDialog.getExistingDirectory(
            self, "Выберите папку с музыкой", os.path.expanduser("~")
        )

        if folder_path:
            self.load_dataset(folder_path)

    def select_annotation_file(self) -> None:
        """Выбрать файл CSV с аннотацией"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл аннотации (CSV)",
            os.path.expanduser("~"),
            "CSV Files (*.csv);;Text Files (*.txt)",
        )

        if file_path:
            self.load_dataset(file_path)

    def load_dataset(self, source_path: str) -> None:
        """Загружает треки из папки для дальнейшей обработки"""
        try:
            if not os.path.exists(source_path):
                self.title_label.setText(f"Путь не существует: {source_path}")
                return
            self.file_iterator = FilePathIterator(source_path)

            if not self.file_iterator._paths:
                self.title_label.setText("Итератор не загрузил пути")
                return

            if source_path.endswith(".csv"):
                csv_dir = os.path.dirname(os.path.abspath(source_path))
                corrected_paths = []

                for path in self.file_iterator._paths:
                    if os.path.isfile(path):
                        corrected_paths.append(path)
                    else:
                        filename = os.path.basename(path)
                        source_folder = os.path.join(csv_dir, "соурс")
                        corrected_path = os.path.join(source_folder, filename)

                        if os.path.isfile(corrected_path):
                            corrected_paths.append(corrected_path)

                self.file_iterator._paths = corrected_paths

            if not self.file_iterator._paths:
                self.title_label.setText("Файлы не найдены после коррекции путей")
                return

            count = len(self.file_iterator._paths)
            self.source_label_info.setText(f"Загружено: {count} файлов")
            self.play_button.setEnabled(True)
            self.prev_button.setEnabled(True)

            first_track_path = self.file_iterator._paths[0]
            self.file_iterator._index = 1
            self.play_file(first_track_path)

        except Exception as e:
            self.title_label.setText(f"Ошибка: {str(e)}")

    def show_next(self) -> None:
        """Показать и играть следующую композицию"""
        if not self.file_iterator:
            return

        try:
            self.current_file_path = next(self.file_iterator)
            self.play_file(self.current_file_path)
        except StopIteration:
            self.file_iterator._index = 0
            self.title_label.setText("Конец плейлиста. Начало повторения...")
            self.info_label.setText("")

    def show_previous(self) -> None:
        """Показать и играть предыдущую композицию (на 1 трек назад)"""
        if not self.file_iterator:
            return

        current_index = self.file_iterator._index - 1
        if current_index > 0:
            new_index = current_index - 1
            paths = self.file_iterator._paths
            if 0 <= new_index < len(paths):
                self.current_file_path = paths[new_index]
                self.file_iterator._index = new_index + 1
                self.play_file(self.current_file_path)

    def play_file(self, file_path: str) -> None:
        """Воспроизвести файл"""
        if not os.path.isfile(file_path):
            self.title_label.setText("Файл не найден")
            return

        url = QUrl.fromLocalFile(file_path)
        media_content = QMediaContent(url)
        self.player.setMedia(media_content)
        self.player.setVolume(80)
        self.player.play()

        self.is_paused = False
        self.pause_button.setText("⏸ Пауза")
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)

        file_name = os.path.basename(file_path)
        title = os.path.splitext(file_name)[0]
        self.title_label.setText(title)

        current_idx = self.file_iterator._index
        total_files = len(self.file_iterator._paths)
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        self.info_label.setText(
            f"Трек {current_idx} из {total_files} | Размер: {file_size_mb:.2f} MB"
        )

    def toggle_pause(self) -> None:
        """Переключение между паузой и воспроизведением"""
        if self.is_paused:
            self.player.play()
            self.pause_button.setText("⏸ Пауза")
            self.is_paused = False
        else:
            self.player.pause()
            self.pause_button.setText("▶ Продолжить")
            self.is_paused = True

    def stop_playback(self):
        """Остановить воспроизведение"""
        self.player.stop()
        self.progress_slider.setValue(0)
        self.time_label.setText("0:00")
        self.is_paused = False
        self.pause_button.setText("⏸ Пауза")
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)

    def on_position_changed(self, position: int) -> None:
        """Обновляет слайдер и текущее время"""
        if not self.progress_slider.isSliderDown():
            self.progress_slider.setMaximum(self.player.duration())
            self.progress_slider.setValue(position)

        time_str = self.format_time(position)
        self.time_label.setText(time_str)

    def on_duration_changed(self, duration: int) -> None:
        """Обновляет максимальное значение слайдера и общее время"""
        self.progress_slider.setMaximum(duration)
        time_str = self.format_time(duration)
        self.duration_label.setText(time_str)

    def on_slider_moved(self, value: int) -> None:
        """Перемотка музыки при перемещении слайдера"""
        self.player.setPosition(value)

    def format_time(self, milliseconds: int) -> str:
        """Конвертирует миллисекунды в формат MM:SS"""
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"


def main():
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
