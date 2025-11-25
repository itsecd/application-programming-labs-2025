import argparse
import sys
from PyQt5.QtWidgets import (
    QWidget, QApplication, 
    QMainWindow,QLabel, 
    QPushButton, QVBoxLayout, 
    QHBoxLayout, QMessageBox, 
    QSlider
)

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QPainter, QPixmap, QIcon

from iterator import FilePathIterator
from pathlib import Path


def create_app() -> QApplication:
    """Инициализирует и возвращает экземпляр QApplication."""
    app = QApplication(sys.argv)

    return app

class Background(QWidget):
    """
    Пользовательский QWidget, используемый в качестве основного фона, 
    отображает изображение на весь экран.
    """
    def __init__(self):
        """Загружает изображение фона из файла."""
        super().__init__()
        self.bg = QPixmap("./back-ground.jpg")

    def paintEvent(self, _):
        """Перерисовывает фоновое изображение, растягивая его на весь виджет."""
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.bg)

class PlayAudioWinDow(QMainWindow):
    """
    Главное окно аудиоплеера, реализующее функции воспроизведения,
    паузы, переключения треков и управления ползунком времени.
    """
    def __init__(self, dataset_path: Path):
        """Конструктор окна аудиоплеера."""
        super().__init__()

        self.paths = list(FilePathIterator(dataset_path))
        self.index = -1 

        self.play = QMediaPlayer(self)
        self.label_title = QLabel("Name: ...")
        self.label_duration = QLabel("Duration: ...")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)

        self.but_prev = QPushButton()
        self.but_play = QPushButton()
        self.but_stop = QPushButton()
        self.but_next = QPushButton()
        
        self.but_prev.setIcon(QIcon("./skip_prev.png"))
        self.but_play.setIcon(QIcon("./play_arrow.png"))
        self.but_stop.setIcon(QIcon("./stop.png"))
        self.but_next.setIcon(QIcon("./skip_next.png"))

        self.setting_ui()

        self.connect_signals()        

    def setting_ui(self) -> None:
        """Создаёт и настраивает графический интерфейс: фон, метки, кнопки и ползунок."""
        self.setFixedSize(550, 350)
        central = Background()
        layout = QVBoxLayout()
        central.setLayout(layout)

        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(18)

        label_style = """
            QLabel {
                color: #DDDDDD;
                font-size: 16px;
                font-weight: bold;
            }
        """

        self.label_title.setStyleSheet(label_style)
        self.label_duration.setStyleSheet(label_style)   
        layout.addWidget(self.label_title)
        layout.addWidget(self.label_duration)

        layout.addWidget(self.slider)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px #999999;
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                stop:0 #B1B1B1, stop:1 #c4c4c4);
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #b4b4b4, stop:1 #8f8f8f);
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }
        """)

        control_row = QHBoxLayout()
        control_row.setSpacing(20)
        control_row.addStretch()
        control_row.addWidget(self.but_prev)
        control_row.addWidget(self.but_play)
        control_row.addWidget(self.but_stop)
        control_row.addWidget(self.but_next)
        control_row.addStretch()
        layout.addLayout(control_row)
        
        button_style = """
        QPushButton {
            background: #111;
            border-radius: 10px;
            padding: 6px 12px;
            font-size: 14px;
        }
        QPushButton:hover{
            background: rgba(255,255,255,230)
        }
        QPushButton:pressed {
            background: rgba(230,230,230,200);
        }
        """

        self.but_prev.setStyleSheet(button_style)
        self.but_play.setStyleSheet(button_style)
        self.but_stop.setStyleSheet(button_style)
        self.but_next.setStyleSheet(button_style)
        self.setCentralWidget(central)
        self.setWindowTitle("Lab 4 - Play Audio(19)")        
    
    
    def connect_signals(self) -> None:
        """Подключает кнопки и сигналы QMediaPlayer к соответствующим обработчикам."""
        self.but_prev.clicked.connect(self.prev_audio)
        self.but_play.clicked.connect(self.play_clicked)
        self.but_stop.clicked.connect(self.stop_clicked)
        self.but_next.clicked.connect(self.next_audio)

        self.play.durationChanged.connect(self.duration_changed)
        self.play.positionChanged.connect(self.update_slider)
        self.play.durationChanged.connect(self.update_range)
        self.slider.sliderMoved.connect(self.seek_position)

    def prev_audio(self)->None:
        """Загружает предыдущий аудиофайл из списка, если он существует."""
        if not self.paths:
            QMessageBox.information(self, "Empty!", "Dataset is empty.")
            return
        
        self.index -= 1

        if self.index < 0: 
            QMessageBox.information(self, "Start!", "No previous compositions.")
            self.index = 0
            return

        self.load_audio(self.paths[self.index])

    def next_audio(self):
        """Загружает следующий аудиофайл из списка, если он существует."""
        if not self.paths:
            QMessageBox.information(self, "Empty!", "Dataset is empty.")
            return
        
        self.index += 1

        if self.index >= len(self.paths):
            QMessageBox.information(self, "End!", "No more compositions.")
            self.index = len(self.paths) - 1
            return

        self.load_audio(self.paths[self.index])
    
    def load_audio(self, path: Path) -> None:
        """Загружает выбранный аудиофайл в QMediaPlayer и обновляет отображаемую информацию."""
        self.play.stop()
        if isinstance(path, dict):
            path = Path(path["abs_path"])
        
        self.cur_path = path

        url = QUrl.fromLocalFile(str(path.resolve()))
        self.play.setMedia(QMediaContent(url))

        self.label_title.setText(f"Name: {path.name}")
        self.label_duration.setText("Duration: ...")

    def play_clicked(self) -> None:
        """Запускает или возобновляет воспроизведение аудиофайла, если файл загружен."""
        if self.play.mediaStatus() == QMediaPlayer.NoMedia:
            return
        self.play.play()

    def stop_clicked(self) -> None:
        """Приостановить текущее аудио."""
        self.play.pause()
    
    def duration_changed(self, ms: int) -> None:
        """Обновляем длительность, когда плеер её узнает."""
        seconds = ms/ 1000.0
        self.label_duration.setText(f"Duration: {seconds:.2f} c")
    
    def update_slider(self, pos) -> None:
        """ Обновляет положение ползунка в соответствии с текущим временем воспроизведения."""
        self.slider.blockSignals(True)
        self.slider.setValue(pos)
        self.slider.blockSignals(False)
    
    def update_range(self, duration) -> None:
        """Устанавливает максимальный диапазон ползунка в соответствии с длительностью трека."""
        self.slider.setRange(0, duration)
    
    def seek_position(self, pos)-> None:
        """Перемещает воспроизведение к выбранной пользователем позиции на ползунке."""
        self.play.setPosition(pos)

def main() -> None:
    """Основная функция."""
    parser = argparse.ArgumentParser(description="Audio player dataset")
    parser.add_argument(
        "--csv",
        help="Path to CSV file or folder with audio files"
    )

    args = parser.parse_args()

    dataset_path = Path(args.csv)

    app = create_app()
    win = PlayAudioWinDow(dataset_path)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()