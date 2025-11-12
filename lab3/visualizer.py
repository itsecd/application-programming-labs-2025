import matplotlib.pyplot as plt
import numpy as np


def plot_audio_comparison(original: np.ndarray,
                          trimmed: np.ndarray,
                          samplerate: int,
                          start_sec: float,
                          end_sec: float) -> None:
    """
    Отображает исходный и обрезанный сигнал аудиофайла.
    """
    duration_full = len(original) / samplerate

    t_full = np.linspace(0, duration_full, num=len(original))
    t_trimmed = np.linspace(start_sec, end_sec, num=len(trimmed))

    plt.figure(figsize=(20, 10))

    plt.subplot(2, 1, 1)
    plt.plot(t_full, original, color="blue")
    plt.title(f"Исходное аудио ({duration_full:.1f} сек)")
    plt.xlabel("Время (сек)")
    plt.ylabel("Амплитуда")

    plt.subplot(2, 1, 2)
    plt.plot(t_trimmed, trimmed, color="green")
    plt.title(f"Обрезанный аудиофайл ({start_sec:.1f}-{end_sec:.1f} сек)")
    plt.xlabel("Время (сек)")
    plt.ylabel("Амплитуда")

    plt.tight_layout()
    plt.show()
