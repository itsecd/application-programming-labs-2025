import argparse
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np

from soundfile_management import (
    file_info,
    remove_silence,
)

from s_math import show_wave


def parse_args() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input", type=str, required=True, help="Путь до исходного аудиофайла"
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output.wav",
        help="Путь для сохранения результата",
    )

    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=0.02,
        help="Порог тишины по амплитуде (0..1 для нормированных данных)",
    )

    return parser.parse_args()


def main() -> None:
    try:
        args = parse_args()
        data, samplerate = sf.read(args.input)
        num_samples, duration = file_info(args.input)
        print(f"Размер аудиофайла: {num_samples} сэмплов, {duration:.2f} с")
        show_wave(data, samplerate, "Исходный сигнал")
        filtered = remove_silence(data, args.threshold)
        if len(filtered) == 0:
            print("После фильтрации не осталось ненулевых участков — проверьте порог.")
        else:
            show_wave(filtered, samplerate, "Сигнал после удаления тишины")
            sf.write(args.output, filtered, samplerate)
            print(f"Результат сохранён в файл: {args.output}")
        plt.show()
    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
