import argparse
from config import ANIMAL_SOUNDS_URL
from file_utils import download_sounds, create_annotation
from iterator import AudioFileIterator
import os
from web_scraper import fetch_animal_sounds


def parse_args():
    """
    Парсит аргументы командной строки.
    """
    parser = argparse.ArgumentParser(
        description="Mixkit animal sounds downloader"
    )
    parser.add_argument(
        "--folder",
        required=True,
        help="Путь к папке для сохранения звуков"
    )
    parser.add_argument(
        "--csv",
        required=True,
        help="Путь к CSV файлу аннотации"
    )
    parser.add_argument(
        "--min_files",
        type=int,
        default=50,
        help="Минимальное количество файлов"
    )
    parser.add_argument(
        "--max_files",
        type=int,
        default=1000,
        help="Максимальное количество файлов"
    )

    return parser.parse_args()


def main():
    """Основная функция скрипта."""
    args = parse_args()

    print("Скачиваем звуки животных с Mixkit.co")
    print(f"Папка: {args.folder}")
    print(f"Аннотация: {args.csv}")
    print(f"Цель: от {args.min_files} до {args.max_files} файлов")

    print("\nИщем звуки животных...")
    sounds = fetch_animal_sounds(ANIMAL_SOUNDS_URL, args.max_files)

    if not sounds:
        print("Не найдено звуков животных")
        return

    print(f"\nВсего найдено звуков: {len(sounds)}")

    print("\nСкачивание звуков...")
    downloaded_files = download_sounds(sounds, args.folder)

    print("\nСоздание аннотации...")
    create_annotation(downloaded_files, args.csv)

    if len(sounds) < args.min_files:
        print(f"\nВНИМАНИЕ: Скачано только {len(sounds)} файлов "
              f"из минимально требуемых {args.min_files}")
    else:
        print(f"Скачано {len(sounds)} файлов")

    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ИТЕРАТОРА")
    print("=" * 50)

    print("\nИтератор из файла аннотации:")
    iterator_csv = AudioFileIterator(args.csv)
    print(f"Всего файлов в итераторе: {len(iterator_csv)}")

    print("\nПервые 5 файлов:")
    for i, path in enumerate(iterator_csv):
        if i < 5:
            print(f"  {i+1}. {os.path.basename(path)}")
        else:
            break

    print("\nИтератор из папки:")
    iterator_folder = AudioFileIterator(args.folder)
    print(f"Всего файлов в итераторе: {len(iterator_folder)}")

    print("\nПервые 5 файлов:")
    for i, path in enumerate(iterator_folder):
        if i < 5:
            print(f"  {i+1}. {os.path.basename(path)}")
        else:
            break


if __name__ == "__main__":
    main()
