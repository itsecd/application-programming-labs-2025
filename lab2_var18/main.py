"""Основной модуль программы."""
import argparse
from settings import HUMAN_SOUNDS_URL
from file_manager import download_human_sounds, create_sounds_annotation
from iterator import AudioFileIterator
from content_fetcher import collect_human_sounds


def parse_args() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.

    Returns:
        Объект с аргументами
    """
    parser = argparse.ArgumentParser(
        description="Скачать звуки человека и создать аннотацию"
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
    return parser.parse_args()


def main() -> None:
    """Основная функция программы."""
    try:
        args = parse_args()

        print("Начало сбора звуков людей...")
        sounds = collect_human_sounds(HUMAN_SOUNDS_URL)

        if not sounds:
            print("Не удалось собрать звуки людей")
            return

        print(f"Найдено звуков для скачивания: {len(sounds)}")

        print("Скачивание звуков...")
        downloaded_files = download_human_sounds(sounds, args.folder)

        print("Создание аннотации...")
        create_sounds_annotation(downloaded_files, args.csv)

        print(f"Успешно скачано {len(downloaded_files)} звуков человека")
        print(f"Аннотация создана: {args.csv}")

        # Демонстрация работы итератора
        print("\nДемонстрация работы итератора:")
        iterator = AudioFileIterator(args.csv)
        print(f"Итератор содержит {len(iterator)} файлов")

    except Exception as e:
        print(f"Критическая ошибка в работе программы: {e}")


if __name__ == "__main__":
    main()