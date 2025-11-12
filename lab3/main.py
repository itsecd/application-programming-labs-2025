import argparse
from audio_utils import (
    load_audio,
    get_duration,
    validate_range,
    trim_audio,
    save_audio,
)

from visualizer import plot_audio_comparison


def parse_args():
    """
    Парсит аргументы командной строки
    """

    parser = argparse.ArgumentParser(
        description="Обрезка аудио в заданном диапазоне"
    )

    parser.add_argument("--input", required=True,
                        help="Путь к исходному файлу")
    parser.add_argument("--output", required=True,
                        help="Путь для сохранения файла")
    parser.add_argument("--start", type=float, required=True,
                        help="Начало диапазона(сек)")
    parser.add_argument("--end", type=float, required=True,
                        help="Конец диапазона(сек)")

    return parser.parse_args()


def main():
    try:
        args = parse_args()

        try:
            data, samplerate = load_audio(args.input)
        except FileNotFoundError:
            print(f"Ошибка: файл '{args.input}' не найден.")
            return
        except Exception as e:
            print(f"Ошибка при загрузке аудио: {e}")
            return

        try:
            duration = get_duration(data, samplerate)
            print(f"Длительность исходного аудиофайла: {duration:.2f} сек.")
        except Exception as e:
            print(f"Ошибка определения длительности аудио: {e}")
            return

        if not validate_range(args.start, args.end, duration):
            print("Ошибка: некорректный диапазон.")
            return

        try:
            trimmed_audio = trim_audio(data, samplerate, args.start, args.end)
        except Exception as e:
            print(f"Ошибка при обрезке аудио: {e}")

        try:
            save_audio(trimmed_audio, samplerate, args.output)
            print(f"Обрезанное аудио сохранено в: {args.output}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

        try:
            plot_audio_comparison(data, trimmed_audio,
                                  samplerate, args.start, args.end)
        except Exception as e:
            print(f"Ошибка визуализации: {e}")
    except KeyboardInterrupt:
        print("\nПроцесс прерван пользователем.")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")


if __name__ == "__main__":
    main()
