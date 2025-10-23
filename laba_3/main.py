import argparse
import os
import sys

from config import logger
from audio_processor import transformations
from visualizer import plot_audio

def parser_t() -> tuple[str, str, str, int]:
    """
    Позволяет через консоль запускать код с аргументами
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=str, help="Путь к файлу для работы с ним")
    parser.add_argument("output_file", type=str, help="Путь для сохранения картинки")
    parser.add_argument("music", type=str, help="Путь для сохранения музыки")
    parser.add_argument("alpha", type=int, help="Число для ускорения")
    args = parser.parse_args()
    return args.source, args.output_file, args.music, args.alpha


def main():
    try:
        source, output_plot, output_audio, alpha = parser_t()

        if alpha < 1:
            raise ValueError("alpha должен быть ≥ 1")

        size = os.path.getsize(source)
        logger.info(f"Размер файла: {size} байт")

        data, data_sped, t_orig, t_sped = transformations(source, output_audio, alpha)
        plot_audio(data, data_sped, t_orig, t_sped, alpha, output_plot)

    except Exception as e:
        logger.error(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
