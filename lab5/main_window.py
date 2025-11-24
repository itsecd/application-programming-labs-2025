import os
import soundfile as sf
from PyQt5.QtCore import QUrl   # указание пути к файлу в плеере
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox   # запуск, класс, выбор CSV через папки, сообщения
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent   # создание плеера, загрузка аудиотрека в плеер

from window_design import Ui_MainWindow
from itr import SoundtrackIterator


class MainWindow(QMainWindow):
    """Главное окно приложения."""

    def __init__(self) -> None:
        """Инициализация окна, плеера и подключение сигналов."""
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.player = QMediaPlayer()
        
        self.current_audio_path = None
        self.iterator = None
        self.track_duration_ms = 0

        # Кнопки
        self.ui.btnChooseFile.clicked.connect(self.load_csv)
        self.ui.btnChooseFolder.clicked.connect(self.load_data)
        self.ui.btnNext.clicked.connect(self.load_next_track)
        self.ui.btnPrev.clicked.connect(self.load_prev_track)
        self.ui.btnPlay.clicked.connect(self.play_audio)
        self.ui.btnStop.clicked.connect(self.stop_audio)

        # Ползунки
        self.ui.sliderProgress.sliderMoved.connect(self.set_position)
        self.ui.sliderVolume.valueChanged.connect(self.set_volume)

        # Сигналы плеера
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)

        # Громкость
        self.player.setVolume(20)
        self.ui.sliderVolume.setValue(20)

    
    def load_csv(self) -> None:
        """Загрузка CSV аннотации и создание итератора."""
        filename, _ = QFileDialog.getOpenFileName(self, "Выберите CSV аннотацию", "", "CSV Files (*.csv)")
        if not filename:
            return
        try:
            self.iterator = SoundtrackIterator(filename)
            self.setWindowTitle(f"Music Viewer – {os.path.basename(filename)}")
            self.reset_labels()
            QMessageBox.information(self, "Готово", "Аннотация успешно загружена!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить CSV:\n{e}")


    def reset_labels(self) -> None:
        """Сброс всех информационных полей."""
        self.ui.lblTitle.setText("-")
        self.ui.lblDuration.setText("-")
        self.ui.lblPath.setText("-")
        self.ui.lblTrackNum.setText("-")
        self.ui.lblCurrentTime.setText("0:00")
        self.ui.lblTotalTime.setText("0:00")

    
    def load_data(self) -> None:
        """Загрузка CSV датасета и создание итератора."""
        filename, _ = QFileDialog.getOpenFileName(self, "Выберите CSV файл с датасетом", "", "CSV Files (*.csv)")
        if not filename:
            return
        try:
            self.iterator = SoundtrackIterator(filename)
            self.setWindowTitle(f"Music Viewer – {os.path.basename(filename)}")
            self.reset_labels()
            QMessageBox.information(self, "Готово", "Датасет загружен!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить датасет:\n{e}")

    
    def load_next_track(self) -> None:
        """Загрузка следующего трека и воспроизведение."""
        if not self.iterator:
            QMessageBox.warning(self, "Нет данных", "Сначала загрузите аннотацию.")
            return
        row = next(self.iterator, None)
        if row is None:
            QMessageBox.information(self, "Конец списка", "Это последний трек.")
            return
        self.load_track(row)
        self.play_audio()


    def load_prev_track(self) -> None:
        """Загрузка предыдущего трека и воспроизведение."""
        if not self.iterator:
            QMessageBox.warning(self, "Нет данных", "Сначала загрузите аннотацию.")
            return
        row = self.iterator.previous()
        if row is None:
            QMessageBox.information(self, "Начало списка", "Это первый трек.")
            return
        self.load_track(row)
        self.play_audio()


    def load_track(self, row: dict) -> None:
        """Загрузка выбранного трека и обновление интерфейса."""
        path = row["Абсолютный путь"]
        if not os.path.exists(path):
            QMessageBox.warning(self, "Ошибка", f"Файл не найден:\n{path}")
            return
        self.current_audio_path = path
        self.stop_audio()

        # Информация о треке, обновление UI
        self.ui.lblTitle.setText(os.path.basename(path))         # название трека
        duration_sec = self.get_duration(path)                   
        self.ui.lblDuration.setText(f"{duration_sec:.2f} сек")   # длительность трека
        self.ui.lblPath.setText(path)                            # путь к треку
        idx = self.iterator._index if self.iterator else 0
        total = self.iterator.length() if self.iterator else 0
        self.ui.lblTrackNum.setText(f"{idx} / {total}")          # количество треков

        # Ползунок
        self.ui.sliderProgress.setValue(0)
        self.ui.lblCurrentTime.setText("0:00")
        self.ui.lblTotalTime.setText(self.format_time(int(duration_sec * 1000)))

        # Загрузка в плеер
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))

   
    def play_audio(self) -> None:
        """Воспроизведение текущего трека."""
        if self.current_audio_path:
            self.player.play()


    def stop_audio(self) -> None:
        """Пауза воспроизведения."""
        self.player.pause()

    
    def set_volume(self, val: int) -> None:
        """Установка громкости плеера."""
        self.player.setVolume(val)

    
    def update_position(self, pos_ms: int) -> None:
        """
        Обновление позиции ползунка трека. 

        Вызывается 25-50 раз в секунду при движении ползунка и не мешает set_position.
        """
        self.ui.sliderProgress.blockSignals(True)
        self.ui.sliderProgress.setValue(pos_ms)
        self.ui.sliderProgress.blockSignals(False)
        self.ui.lblCurrentTime.setText(self.format_time(pos_ms))


    def update_duration(self, dur_ms: int) -> None:
        """Обновление длительности трека."""
        self.track_duration_ms = dur_ms
        self.ui.sliderProgress.setRange(0, dur_ms)
        self.ui.lblTotalTime.setText(self.format_time(dur_ms))


    def set_position(self, pos_ms: int) -> None:
        """Перемотка трека."""
        self.player.setPosition(pos_ms)


    def get_duration(self, filepath: str) -> float:
        """Получение длительности трека в секундах."""
        try:
            data, sr = sf.read(filepath)
            return len(data) / sr
        except Exception:
            return 0.0


    def format_time(self, ms: int) -> str:
        """Форматирование миллисекунд в M:SS."""
        sec = ms // 1000
        m = sec // 60
        s = sec % 60
        return f"{m}:{s:02d}"


def main() -> None:
    """Запуск приложения."""
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()


if __name__ == "__main__":
    main()
