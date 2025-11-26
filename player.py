from PyQt5 import QtWidgets, uic
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QFileDialog
import os
from mutagen.id3 import ID3


class MusicPlayer(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        """
        Инициализация плеера
        """
        super().__init__()
        uic.loadUi("player.ui", self)

        self.setWindowIcon(QIcon("Assets/icon_1.png"))
        self.player = QMediaPlayer()
        self.tracks = []
        self.current_track_index = 0

        self.Play_button.clicked.connect(self.play)
        self.Stop_button.clicked.connect(self.pause_play)
        self.NextTrack_button.clicked.connect(self.next_track)
        self.PrevTrack_button.clicked.connect(self.prev_track)
        self.soundSlider.valueChanged.connect(self.volume_Change)
        self.addButton.clicked.connect(self.browse_dir)
        self.music_Slider.sliderMoved.connect(self.move_pos)
        self.player.mediaStatusChanged.connect(self.next_if_stop)

        self.timer = QTimer()
        self.player.positionChanged.connect(self.update_progress)
        self.player.durationChanged.connect(self.update_duration)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_track_index >= len(self.tracks):
            raise StopIteration
        result = self.tracks[self.current_track_index]
        self.current_track_index += 1
        return result

    def prev(self) -> None:
        if self.current_track_index <= 0:
            raise IndexError("Неверный индекс")
        self.current_track_index -= 1
        return self.tracks[self.current_track_index]

    def browse_dir(self) -> None:
        """
        Диалоговое окно для выбора директории
        """
        try:
            dir = QFileDialog.getExistingDirectory(self)
            self.load_from_dir(dir)
        except Exception as e:
            print(f"Произошла ошибка {e}")

    def load_from_dir(self, path: str) -> None:
        """
        Получает все музыкальные файлы
        """
        for filename in os.listdir(path):
            if filename.endswith((".mp3", ".wav")):
                abs_path = os.path.join(path, filename)

                self.tracks.append({"filename": filename, "absolute_path": abs_path})

    def set_cover_to_label(self):
        try:
            track = self.tracks[self.current_track_index]
            tags = ID3(track.get("absolute_path"))
            pic = tags["APIC:Album Cover"]
            pixmap = QPixmap()
            pixmap.loadFromData(pic.data)
            self.AlbumCoverLabel.setPixmap(pixmap)
            self.AlbumCoverLabel.setScaledContents(True)
        except Exception:
            self.AlbumCoverLabel.setPixmap(QPixmap("Assets/NOT_FOUND.jpg"))

    def play(self) -> None:
        """
        Функция для включения трека
        """
        if len(self.tracks) > 0:
            track = self.tracks[self.current_track_index]
            file_path = track.get("absolute_path")
            url = QUrl.fromLocalFile(os.path.abspath(file_path))
            title = track.get("filename", "Unknown")[:-4]
            media = QMediaContent(url)
            self.player.setMedia(media)
            self.player.play()
            self.timer.start()
            self.MusicName_label.setText(f"{title}")
            self.set_cover_to_label()

    def pause_play(self) -> None:
        """
        Функция для остановки трека
        """
        state = self.player.state()
        if state == QMediaPlayer.PlayingState:
            self.player.pause()
        elif state == QMediaPlayer.PausedState:
            self.player.play()
        else:
            self.play()

    def next_track(self) -> None:
        """
        Функция для переключения на следующий трек
        """
        try:
            next(self)
            self.play()
        except StopIteration:
            print("Произошла ошибка")

    def prev_track(self) -> None:
        """
        Функция для переключения на предыдущий трек
        """
        try:
            self.prev()
            self.play()
        except IndexError as e:
            print(f"Произошла ошибка: {e}")

    def update_progress(self, position: float) -> None:
        """
        Функция для обновления прогресса в progress bar и таймера
        """
        dur = self.player.duration()
        pos = self.player.position()

        if dur > 0:
            self.music_Slider.setValue(int(pos))
            pos_sec = pos // 1000
            dur_sec = dur // 1000
            self.TimerLabel.setText(
                f"{pos_sec // 60:02}:{pos_sec % 60:02} / {dur_sec // 60:02}:{dur_sec % 60:02}"
            )

    def update_duration(self, duration: int) -> None:
        """
        Максимум для прогресса
        """
        if hasattr(self, "music_Slider"):
            self.music_Slider.setMaximum(duration)

    def move_pos(self, value: float) -> None:
        """
        Позволяет работать с положением трека с помощью слайдера
        """
        self.player.setPosition(value)

    def next_if_stop(self, status):
        """
        Запускает следующий трек если предыдущий окончен
        """
        if status == QMediaPlayer.EndOfMedia:
            self.next_track()

    def volume_Change(self) -> None:
        """
        Меняем громкость слайдером
        """
        volume_val = self.soundSlider.value()
        self.player.setVolume(volume_val)
        self.volume_Label.setText(str(volume_val))
