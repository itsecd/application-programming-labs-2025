import matplotlib.pyplot as plt
import numpy as np


def plot_comparison(
    original: np.ndarray, processed: np.ndarray, sample_rate: int
) -> None:
    """Строит графики сравнения исходного и обработанного аудио."""
    samples_to_show = min(len(original), 2 * sample_rate)
    time = np.linspace(0, 2, samples_to_show)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

    ax1.plot(time, original[:samples_to_show], 'b-', linewidth=0.8)
    ax1.set_title('Исходное аудио')
    ax1.set_ylabel('Амплитуда')
    ax1.grid(True, alpha=0.3)

    ax2.plot(time, processed[:samples_to_show], 'r-', linewidth=0.8)
    ax2.set_title('Аудио с ограниченной амплитудой')
    ax2.set_xlabel('Время (секунды)')
    ax2.set_ylabel('Амплитуда')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()