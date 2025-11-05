import matplotlib.pyplot as plt
import numpy as np


def visualize(original: np.ndarray,echo: np.ndarray,delay_samples: int,samplerate: int,) -> None:
    """Визуализирует исходный и обработанный сигналы"""

    samples_to_show = min(samplerate * 2, len(original))
    time_axis = np.arange(samples_to_show) / samplerate

    plt.figure(figsize=(14, 8))

    plt.subplot(2, 1, 1)
    plt.plot(
        time_axis,
        original[:samples_to_show],
        color="blue",
        linewidth=0.5,
    )
    plt.title("Исходный сигнал", fontsize=12, fontweight="bold")
    plt.xlabel("Время (сек)")
    plt.ylabel("Амплитуда")
    plt.grid(True, alpha=0.3)
    plt.ylim(-1.1, 1.1)

    plt.subplot(2, 1, 2)
    echo_to_show = min(samples_to_show, len(echo))
    plt.plot(
        time_axis[:echo_to_show],
        echo[:echo_to_show],
        color="green",
        linewidth=0.5,
    )
    plt.title("Сигнал с эхо-эффектом", fontsize=12, fontweight="bold")
    plt.xlabel("Время (сек)")
    plt.ylabel("Амплитуда")
    plt.grid(True, alpha=0.3)
    plt.ylim(-1.1, 1.1)

    delay_seconds = delay_samples / samplerate
    plt.figtext(
        0.5,
        0.02,
        f"Задержка: {delay_seconds:.3f} сек ({delay_samples} сэмплов)",
        ha="center",
        fontsize=10,
    )

    plt.tight_layout()
    plt.show()
    
    
