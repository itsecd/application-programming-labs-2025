import argparse
import os

import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt


def args_parse() -> argparse.Namespace:
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        prog="Data parser",
        description="Parsing data from file"
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Path to input audio file"
    )
    parser.add_argument(
        "-i", "--image",
        type=str,
        help="Path to save the plot image"
    )
    parser.add_argument(
        "-o", "--output_audio",
        type=str,
        help="Path to save processed audio"
    )
    parser.add_argument(
        "-a", "--alpha",
        type=int,
        help="Speed increase factor"
    )
    return parser.parse_args()


def process_audio(
    input_file: str,
    output_file: str,
    alpha: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Ускоряет музыку input_file в альфа раз и сохраняет как output_file.
    """
    data, samp = sf.read(input_file)
    data_alpha = data[::alpha]

    time_origin = np.arange(len(data)) / samp
    time_alpha = np.arange(len(data_alpha)) / samp

    sf.write(output_file, data_alpha, samp, format="WAV")

    return data, data_alpha, time_origin, time_alpha


def plot_audio(
    data: np.ndarray,
    data_alpha: np.ndarray,
    time_orig: np.ndarray,
    time_alpha: np.ndarray,
    image: str,
) -> None:
    """
    Функция для построения графика.
    """
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(time_orig, data, color='blue')
    plt.title("Исходное аудио")
    plt.xlabel("Время (сек)")
    plt.ylabel("Амплитуда")
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(time_alpha, data_alpha, color='red')
    plt.title("Ускоренное аудио")
    plt.xlabel("Время (сек)")
    plt.ylabel("Амплитуда")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(image)
    plt.close()


def main():
    args = args_parse()

    if not args.file:
        print("Please specify file using -f argument")
        return

    if not args.output_audio:
        print("Please specify output audio using -o argument")
        return

    if not args.image:
        print("Please specify image using -i argument")
        return

    if not args.alpha:
        print("Please specify alpha using -a argument")
        return

    if args.alpha < 1:
        raise ValueError("alpha должен быть ≥ 1")

    if not os.path.exists(args.file):
        print(f"Input file {args.file} does not exist!")
        return

    size = os.path.getsize(args.file)
    print("Размер файла в байтах:", size)

    data_orig, data_alpha, t_orig, t_alpha = process_audio(
        args.file, args.output_audio, args.alpha
    )

    plot_audio(data_orig, data_alpha, t_orig, t_alpha, args.alpha, args.image)


if __name__ == "__main__":
    main()