import os
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
import argparse
from laba_2.main import FilePathIterator
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s %(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def parser_t() -> tuple[str, str, str, int]:
    """
    Позволяет через консоль запускать код с аргументами
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str,
                        help='Путь к файлу для работы с ним')
    parser.add_argument('output_file', type=str,
                        help='Путь для сохранения картинки')
    parser.add_argument('music', type=str,
                        help='Путь для сохранения музыки')
    parser.add_argument('alpha', type=int,
                        help='Число для ускорения')
    args = parser.parse_args()
    return args.source, args.output_file, args.music, args.alpha

def transformations(source, music: str, alpha: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Функция увеличивает музыку в alpha раз
    """
    data, samplerate = sf.read(source)
    data_sped = data[::alpha]
    t_orig = np.arange(len(data))     / samplerate
    t_sped = np.arange(len(data_sped)) / samplerate
    sf.write(music, data_sped, samplerate, format="WAV")
    return data, data_sped, t_orig, t_sped

def plot_audio(data, data_sped, t_orig, t_sped, alpha: int, output_plot: str) -> None:
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

def main():
    try:
        source, output_plot, output_audio, alpha = parser_t()

        if alpha < 1:
            raise ValueError("alpha должен быть ≥ 1")
        
        size = os.path.getsize(source)
        logging.info(f"Размер файла: {size} байт")

        data, data_sped, t_orig, t_sped = transformations(source, output_audio, alpha)
        plot_audio(data, data_sped, t_orig, t_sped, alpha, output_plot)

    except Exception as e:
        logging.error(e)
        sys.exit(1)
        
if __name__ == '__main__':
    main()