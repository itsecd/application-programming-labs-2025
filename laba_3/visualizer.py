import numpy as np
import matplotlib.pyplot as plt

def plot_audio(data: np.ndarray, data_sped: np.ndarray, t_orig: np.ndarray, 
               t_sped: np.ndarray, alpha: int, output_plot: str) -> None:
    """
    Функция для построения графика
    """
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=False)
    
    axes[0].plot(t_orig, data[:, 0], color='blue')
    axes[0].set_title('Исходное аудио')
    axes[0].set_ylabel('Амплитуда')
    axes[0].axhline(0, color="black", ls="--")
    
    axes[1].plot(t_sped, data_sped[:, 0], color='green')
    axes[1].set_title(f'Ускорённое аудио (×{alpha})')
    axes[1].set_xlabel('Время, сек')
    axes[1].set_ylabel('Амплитуда')
    axes[1].axhline(0, color="black", ls="--")
    
    plt.tight_layout()
    plt.savefig(output_plot, dpi=300, bbox_inches='tight')
    plt.show()
