import numpy as np
import soundfile as sf
import argparse
import matplotlib.pyplot as plt


def parser() -> argparse.Namespace:
    """
    Парсит аргументы командной строки
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str, help="Путь до аудио файла")

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output.mp3",
        help="Название обрезанного файла",
    )

    parser.add_argument("-s", "--start", type=int, help="Начало файла (В секундах)")

    parser.add_argument("-e", "--end", type=int, help="Конец файла (В секундах)")

    return parser.parse_args()


def trim_audio(path: str, start: int, end: int, output: str) -> None:
    """
    Осуществляет обрезку аудио
    """
    try:
        data, samplerate = sf.read(path)
        num_samples, minutes, sec = file_info(path)

        if end > ((minutes * 60) + sec):
            raise ValueError("Нельзя отрезать больше положенного ;)")
        if start < 0:
            raise ValueError("Нельзя добавить больше положенного ;)")

        start_sample = samplerate * start
        end_sample = samplerate * end

        trim = data[start_sample:end_sample]
        sf.write(output, trim, samplerate)
    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")


def file_info(path: str) -> tuple[int, int, int]:
    """
    Возвращает информацию о файле
    """
    try:
        data, samplerate = sf.read(path)
        num_samples = len(data)
        duration = num_samples / samplerate

        minutes = int(duration // 60)
        sec = int(duration % 60)

        return num_samples, minutes, sec
    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")


def show_wave(path: str, title: str) -> None:
    data, sr = sf.read(path)
    if len(data.shape) == 2:
        data = data[:, 0]
    times = np.arange(len(data)) / sr

    plt.figure(figsize=(12, 4))
    plt.plot(times, data)
    plt.title(title)
    plt.ylabel("Амплитуда")
    plt.xlabel("Время в секундах")
    plt.tight_layout()
    plt.show()


def main() -> None:
    try:
        args = parser()
        num_samples, minutes, sec = file_info(args.input)
        print(f"Размер аудиофайла: {num_samples} сэмплов")
        trim_audio(args.input, args.start, args.end, args.output)
        show_wave(args.output, "Обрезанный файл")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
