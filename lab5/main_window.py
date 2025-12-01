import os
import sys
from typing import Optional
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from iter import SoundtrackIterator


class SimpleAudioPlayer(QMainWindow):
    """Главное окно аудиоплеера для воспроизведения треков из CSV."""
    
    def __init__(self) -> None:
        """Инициализация главного окна приложения."""
        super().__init__()
        
        self.iterator: Optional[SoundtrackIterator] = None
        self.player: QMediaPlayer = QMediaPlayer()

        self.setWindowTitle("Аудиоплеер")
        self.setFixedSize(500, 400)
        
        self.create_widgets()
        
        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)
        
    def create_widgets(self) -> None:
        """Создает и настраивает все элементы интерфейса."""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        
        self.select_btn = QPushButton("Открыть CSV")
        self.select_btn.clicked.connect(self.open_csv)
        layout.addWidget(self.select_btn)
        
        self.info_label = QLabel("Выберите CSV файл")
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.sliderMoved.connect(self.set_position)
        self.slider.setEnabled(False)
        layout.addWidget(self.slider)
        
        self.time_label = QLabel("0:00 / 0:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.time_label)
        
        controls = QHBoxLayout()
        
        self.play_btn = QPushButton("▶")
        self.play_btn.clicked.connect(self.play_pause)
        self.play_btn.setEnabled(False)
        
        self.stop_btn = QPushButton("■")
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.setEnabled(False)
        
        self.next_btn = QPushButton("→")
        self.next_btn.clicked.connect(self.next_track)
        self.next_btn.setEnabled(False)
        
        controls.addWidget(self.play_btn)
        controls.addWidget(self.stop_btn)
        controls.addWidget(self.next_btn)
        layout.addLayout(controls)
        
    def open_csv(self) -> None:
        """Открывает диалог выбора CSV файла и загружает данные."""
        filename, _ = QFileDialog.getOpenFileName(
            self, 
            "Открыть CSV", 
            "", 
            "CSV файлы (*.csv)"
        )
        
        if not filename:
            return
            
        try:
            self.iterator = SoundtrackIterator(filename)
            self.next_btn.setEnabled(True)
            self.load_next_track()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл: {str(e)}")
    
    def load_next_track(self) -> None:
        """Загружает следующий трек из итератора."""
        if self.iterator is None:
            return
            
        self.player.stop()
        
        try:
            row = next(self.iterator)
            
            title = row.get('Название', 'Без названия')
            artist = row.get('Исполнитель', 'Неизвестно')
            self.info_label.setText(f"{title}\n{artist}")
            
            filepath = row.get('Абсолютный путь', '')
            if os.path.exists(filepath):
                media_content = QMediaContent(QUrl.fromLocalFile(filepath))
                self.player.setMedia(media_content)
                self.play_btn.setEnabled(True)
                self.slider.setValue(0)
            else:
                QMessageBox.warning(self, "Файл не найден", f"Файл не найден: {filepath}")
                self.load_next_track()
                
        except StopIteration:
            self.info_label.setText("Конец списка")
            self.next_btn.setEnabled(False)
            QMessageBox.information(self, "Конец", "Все треки воспроизведены")
    
    def play_pause(self) -> None:
        """Переключает между воспроизведением и паузой."""
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_btn.setText("▶")
        else:
            self.player.play()
            self.play_btn.setText("⏸")
            self.stop_btn.setEnabled(True)
    
    def stop(self) -> None:
        """Полностью останавливает воспроизведение."""
        self.player.stop()
        self.play_btn.setText("▶")
        self.stop_btn.setEnabled(False)
        self.slider.setValue(0)
    
    def next_track(self) -> None:
        """Загружает следующий трек."""
        self.load_next_track()
    
    def update_duration(self, duration: int) -> None:
        """Обновляет интерфейс при изменении длительности трека."""
        if duration > 0:
            self.slider.setEnabled(True)
            self.format_time(duration)
    
    def update_position(self, position: int) -> None:
        """Обновляет позицию ползунка при изменении позиции воспроизведения."""
        if self.player.duration() > 0:
            progress = int((position / self.player.duration()) * 100)
            self.slider.setValue(progress)
            self.format_time(position)
    
    def format_time(self, current: Optional[int] = None) -> None:
        """Форматирует и отображает текущее и общее время."""
        duration = self.player.duration()
        if current is None:
            current = self.player.position()
        
        if duration > 0:
            c_min = current // 60000
            c_sec = (current % 60000) // 1000
            
            d_min = duration // 60000
            d_sec = (duration % 60000) // 1000
            
            self.time_label.setText(f"{c_min}:{c_sec:02d} / {d_min}:{d_sec:02d}")
    
    def set_position(self, value: int) -> None:
        """Устанавливает позицию воспроизведения по значению ползунка."""
        if self.player.duration() > 0:
            position = int((value / 100) * self.player.duration())
            self.player.setPosition(position)


def main() -> None:
    """Точка входа в приложение."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = SimpleAudioPlayer()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()