import argparse
import os
import sys


def parse_arguments() -> argparse.Namespace:
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description="Переворачивание аудиофайла задом наперед"
    )
    parser.add_argument("input_file", help="Путь к входному аудиофайлу")
    parser.add_argument("output_file", help="Путь для сохранения результата")

    args = parser.parse_args()

    # Проверка существования входного файла
    if not os.path.exists(args.input_file):
        print(f"Ошибка: файл '{args.input_file}' не найден")
        sys.exit(1)

    # Проверка расширения
    if not args.input_file.lower().endswith((".wav", ".flac", ".ogg")):
        print("Внимание: SoundFile лучше всего работает с WAV, FLAC, OGG файлами")
        print(
            "Для MP3 рекомендуется использовать другие библиотеки или конвертировать в WAV"
        )

    return args
