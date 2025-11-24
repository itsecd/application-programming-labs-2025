

import argparse
import os
import sys


print("🔍 Текущий путь Python:", sys.path)
print("📂 Содержимое текущей директории:", os.listdir('.'))


try:
    from crawler import download_monkey_images
    from annotator import create_annotation_csv
    from file_iterator import FileIterator
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("💡 Убедитесь, что файлы crawler.py, annotator.py и file_iterator.py находятся в той же папке, что и main.py.")
    sys.exit(1)

from typing import NoReturn

def parse_args():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(description="Скачивание изображений и создание аннотаций.")
    parser.add_argument(
        "--download-dir",
        type=str,
        default="downloaded_images",
        help="Путь к папке для сохранения изображений (по умолчанию: downloaded_images)"
    )
    parser.add_argument(
        "--annotation-file",
        type=str,
        default="annotations.csv",
        help="Имя CSV-файла для аннотаций (по умолчанию: annotations.csv)"
    )
    parser.add_argument(
        "--max-num",
        type=int,
        default=100,
        help="Максимальное количество изображений (от 50 до 1000)"
    )
    parser.add_argument(
        "--min-num",
        type=int,
        default=50,
        help="Минимальное количество изображений (от 50 до 1000)"
    )
    parser.add_argument(
        "--year",
        type=int,
        default=2025,
        help="Год для фильтрации изображений (по умолчанию: текущий год)"
    )
    parser.add_argument(
        "--use-csv",
        action="store_true",
        help="Использовать существующий CSV-файл вместо скачивания новых изображений"
    )
    parser.add_argument(
        "--source-path",
        type=str,
        help="Путь к CSV-файлу аннотаций или к папке с изображениями для итератора"
    )

    return parser.parse_args()


def main() -> NoReturn:
    """
    Точка входа программы. Выполняет скачивание, аннотацию и итерацию по файлам.
    """
    args = parse_args()

    try:
        print("🚀 Запуск программы...")

        image_dir = args.download_dir
        annotation_file = args.annotation_file

        
        if not args.use_csv:
            image_dir = download_monkey_images(
                keyword="monkey",
                max_num=args.max_num,
                min_num=args.min_num,
                year=args.year
            )

      
        create_annotation_csv(image_dir, annotation_file)

        
        source = args.source_path or annotation_file

        print(f"\n🔄 Итерация по файлам из: {source}")
        file_iter = FileIterator(source)

        for i, path in enumerate(file_iter, 1):
            print(f"{i:>3}. {path}")

        print(f"\n✅ Всего файлов: {len(file_iter)}")

    except KeyboardInterrupt:
        print("\n🛑 Программа прервана пользователем.")
    except Exception as e:
        print(f"💥 Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()