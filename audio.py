import os

import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf


class AudioTrack:
    """Class that reads and works with audio data"""

    def __init__(self, path):
        """Constructor. Accept path to music file"""
        if os.path.isfile(path):
            self.data, self.samplerate = sf.read(path)
            if self.data.ndim == 2:  # Преобразование стерео в моно с помощью усреднения
                self.data = np.mean(self.data, axis=1)
            self.filename = os.path.basename(path)
        else:
            raise FileNotFoundError("The file cannot be opened.")

    def info(self) -> list[int]:
        """Return parametrs of current audio file [samlperate, duration, samples count]"""
        return [self.samplerate, len(self.data) / self.samplerate, len(self.data)]

    def vizualize(self) -> None:
        """Show wave of this audio"""
        duration = len(self.data) / self.samplerate
        time = np.linspace(0, duration, len(self.data))

        plt.figure(figsize=(12, 4))
        plt.plot(time, self.data, linewidth=0.5, alpha=0.7, color="blue")
        plt.title("Исходная аудиоволна")
        plt.xlabel("Время (секунды)")
        plt.ylabel("Амплитуда")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def vizualize(self, audio_file) -> None:
        """Show two wave of audio for compare"""
        duration = len(self.data) / self.samplerate
        time = np.linspace(0, duration, len(self.data))

        plt.figure(figsize=(12, 4))
        plt.plot(time, self.data, linewidth=0.5, alpha=0.7, color="blue")
        plt.title("Исходная аудиоволна")
        plt.xlabel("Время (секунды)")
        plt.ylabel("Амплитуда")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        plt.figure(figsize=(12, 4))
        plt.plot(time, audio_file.data, linewidth=0.5, alpha=0.7, color="red")
        plt.title("Сглаженная аудиоволна")
        plt.xlabel("Время (секунды)")
        plt.ylabel("Амплитуда")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def save(self, path):
        """Save audio track to file"""
        if os.path.exists(path):
            sf.write(os.path.join(path, self.filename), self.data, self.samplerate)
        else:
            try:
                os.makedirs(path, exist_ok=True)
                sf.write(os.path.join(path, self.filename), self.data, self.samplerate)
            except Exception as e:
                raise e


def smooth(track: AudioTrack, window_size: int) -> AudioTrack:
    """Smoothing the audio signal using a moving average via numpy.convolve"""
    window = np.ones(window_size) / window_size
    track.data = np.convolve(track.data, window, mode="same")

    return track
