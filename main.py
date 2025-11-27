import argparse
from trimmer import trim_audio, file_info, show_wave


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
