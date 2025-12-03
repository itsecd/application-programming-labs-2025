import argparse
import os
from downloader import (
    ensure_directory,
    validate_num_images,
    create_crawler,
    download_images
)
from annotation import create_annotation_csv
from iterator_module import FileIterator


def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.

    :return: Объект argparse.Namespace.
    """
    parser = argparse.ArgumentParser(
        description="Скачивание изображений 'hedgehog' "
                    "с выбранного источника и создание файла-аннотации."
    )
    parser.add_argument(
        "--crawler",
        type=str,
        required=True,
        choices=["google", "bing", "flickr"],
        help="Источник загрузки (google | bing | flickr)"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        required=True,
        help="Папка для сохранения изображений"
    )
    parser.add_argument(
        "--num",
        type=int,
        default=100,
        help="Количество изображений (50–1000)"
    )
    parser.add_argument(
        "--csv",
        type=str,
        default="annotation.csv",
        help="Имя CSV-файла с аннотацией"
    )
    return parser.parse_args()


def main() -> None:
    """Главная функция программы."""
    args = parse_arguments()

    try:
        validate_num_images(args.num)
        ensure_directory(args.output_dir)

        crawler = create_crawler(args.crawler, args.output_dir)
        download_images(crawler, args.num)

        create_annotation_csv(args.output_dir, args.csv)

        print("\nИтерация по файлам из аннотации:")
        for path in FileIterator(args.csv):
            print("→", path)

        print("\nПрограмма выполнена успешно.")

    except ValueError as ve:
        print(f"Ошибка ввода: {ve}")
    except RuntimeError as re:
        print(f"Ошибка загрузки: {re}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
