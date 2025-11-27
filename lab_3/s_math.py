import matplotlib.pyplot as plt
import numpy as np


def show_wave(data: np.ndarray, sr: int, title: str) -> None:
    """
    Рисует осциллограмму аудиосигнала.
    """
    if data.ndim == 2:
        data = data[:, 0]
    times = np.arange(len(data)) / sr

    plt.figure(figsize=(10, 3))
    plt.plot(times, data, linewidth=0.8)
    plt.title(title)
    plt.ylabel("Амплитуда")
    plt.xlabel("Время, с")
    plt.tight_layout()
