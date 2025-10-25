import soundfile as sf
import numpy as np

class AudioProcessor:
    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path
        self.data: np.ndarray | None = None
        self.samplerate: int | None = None

    def read_audio(self) -> tuple[np.ndarray, int]:
        self.data, self.samplerate = sf.read(self.file_path)
        print(f"audio size(samples): {len(self.data)}")
        print(f"Time: {len(self.data) / self.samplerate:.2f} sec")
        return self.data, self.samplerate

    def save_audio(self, file_path: str, data: np.ndarray) -> None:
        sf.write(file_path, data, self.samplerate)
        print(f"audio save: {file_path}")

    def change_speed_linear(self, factor: float) -> np.ndarray:
        """
        linear interp
        берется исходный массив сэмплов (значений амплитуд), 
        создается новый массив в factor раз больше и равномерно 
        вычисялется уравнение прямой между двумя старыми точками
        и на основе него между ними вставляются еще сколько-то сэмплов
        """
        signal = self.data
        if factor == 1.0:
            return signal

        n_samples: int = int(len(signal) * factor)
        old_indices: np.ndarray = np.arange(len(signal))
        new_indices: np.ndarray = np.linspace(0, len(signal) - 1, n_samples)

        if signal.ndim == 1:
            new_signal: np.ndarray = np.interp(new_indices, old_indices, signal)
        else:
            new_signal: np.ndarray = np.zeros((n_samples, signal.shape[1]))
            for ch in range(signal.shape[1]):
                new_signal[:, ch] = np.interp(new_indices, old_indices, signal[:, ch])

        return new_signal

    def quadratic_interp(self, factor: float) -> np.ndarray:
        """
        quadratic interp
        берется исходный массив индексов и расширяется в factor раз
        для трех соседних точек вычисляется уравнение параболы,
        на основе него между этими точками вставляются дополнительные сэмплы
        """
        signal = self.data
        if factor <= 0:
            raise ValueError("factor must be > 0")

        n_samples: int = int(len(signal) * factor)
        new_indices: np.ndarray = np.linspace(0, len(signal) - 1, n_samples)

        if signal.ndim == 1:
            new_signal: np.ndarray = np.zeros(n_samples)
            channels: int = 1
        else:
            channels: int = signal.shape[1]
            new_signal: np.ndarray = np.zeros((n_samples, channels))

        for i, x in enumerate(new_indices):
            x1: int = int(np.floor(x))
            x0: int = max(x1 - 1, 0)
            x2: int = min(x1 + 1, len(signal) - 1)

            if channels == 1:
                y0, y1, y2 = signal[x0], signal[x1], signal[x2]
                t: float = x - x0
                a: float = y0 / 2 - y1 + y2 / 2
                b: float = -y0 + y1 - a
                c: float = y0
                new_signal[i] = a * t**2 + b * t + c
            else:
                for ch in range(channels):
                    y0, y1, y2 = signal[x0, ch], signal[x1, ch], signal[x2, ch]
                    t: float = x - x0
                    a: float = y0 / 2 - y1 + y2 / 2
                    b: float = -y0 + y1 - a
                    c: float = y0
                    new_signal[i, ch] = a * t**2 + b * t + c

        return new_signal

