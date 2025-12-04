import argparse
import sys
import os
from downloader import SoundDownloader
from iterator import SoundFileIterator


def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки

    Returns:
        Объект с аргументами
    """
    parser = argparse.ArgumentParser(description='Скачивание звуков животных с mixkit.co')

    parser.add_argument(
        '--download_dir',
        type=str,
        default='animal_sounds',
        help='Директория для сохранения звуков (по умолчанию: animal_sounds)'
    )

    parser.add_argument(
        '--annotation_file',
        type=str,
        default='sound_annotation.csv',
        help='Путь к файлу аннотации (по умолчанию: sound_annotation.csv)'
    )

    parser.add_argument(
        '--max_count',
        type=int,
        default=50,
        help='Максимальное количество звуков для скачивания (по умолчанию: 50)'
    )

    return parser.parse_args()


def demonstrate_iterator(annotation_file: str) -> None:
    """
    Демонстрирует работу итератора

    Args:
        annotation_file: Путь к файлу аннотации
    """
    print("\n" + "=" * 50)
    print("Демонстрация работы итератора:")
    print("=" * 50)

    try:
        sound_iterator = SoundFileIterator(annotation_file)

        print(f"Всего файлов в аннотации: {len(sound_iterator)}")

        for i, (absolute_path, relative_path) in enumerate(sound_iterator, 1):
            print(f"{i}. Абсолютный путь: {absolute_path}")
            print(f"   Относительный путь: {relative_path}")

            if i >= 5:  # Показываем только первые 5 для демонстрации
                print("... и так далее")
                break

    except Exception as e:
        print(f"Ошибка при демонстрации итератора: {e}")


def main() -> None:
    """
    Основная функция программы
    """
    try:
        # Парсим аргументы командной строки
        args = parse_arguments()

        print("=" * 50)
        print("Sound Downloader - Вариант 19")
        print("Тема: Звуки животных")
        print("=" * 50)
        print(f"Директория для сохранения: {args.download_dir}")
        print(f"Файл аннотации: {args.annotation_file}")
        print(f"Количество звуков: {args.max_count}")
        print("=" * 50)

        # Скачиваем звуки
        downloader = SoundDownloader()
        downloader.download_sounds(
            download_dir=args.download_dir,
            annotation_file=args.annotation_file,
            max_count=args.max_count
        )

        # Демонстрируем работу итератора
        if os.path.exists(args.annotation_file):
            demonstrate_iterator(args.annotation_file)
        else:
            print("Файл аннотации не создан, невозможно продемонстрировать итератор")

    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()