import argparse
import sys
from typing import List

from downloader import download_images_by_keywords
from annotator import create_annotation_csv, FileAnnotationIterator
from utils import validate_and_create_dir, calculate_per_keyword_count

def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.

    Returns:
        argparse.Namespace: Объект с аргументами.
    """
    parser = argparse.ArgumentParser(description="Скачивание изображений и создание аннотации.")
    parser.add_argument(
        '--keywords',
        nargs='+',
        required=True,
        help='Список ключевых слов для поиска изображений "cat dog bird"'
    )
    parser.add_argument(
        '--total-images',
        type=int,
        default=100,
        choices=range(50, 1001),
        help='Общее количество изображений для скачивания (от 50 до 1000). По умолчанию: 50.'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./downloaded_images',
        help='Директория для сохранения изображений. По умолчанию: ./downloaded_images'
    )
    parser.add_argument(
        '--annotation-file',
        type=str,
        default='./annotations.csv',
        help='Путь к файлу аннотации. По умолчанию: ./annotations.csv'
    )

    args = parser.parse_args()

    if args.total_images < 50 or args.total_images > 1000:
        parser.error("Количество изображений должно быть от 50 до 1000.")

    return args

def main() -> None:
    """
    Основная функция программы.
    """
    try:
        args = parse_arguments()

        output_dir = validate_and_create_dir(args.output_dir)

        per_keyword_count = calculate_per_keyword_count(args.total_images, args.keywords)

        download_images_by_keywords(args.keywords, str(output_dir), per_keyword_count)

        total_downloaded = 0
        for keyword in args.keywords:
            keyword_dir = output_dir / keyword
            if keyword_dir.exists():
                images = [
                    f for f in keyword_dir.iterdir()
                    if f.is_file() and f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
                ]
                total_downloaded += len(images)
                print(f"Загружено файлов для '{keyword}': {len(images)}")
            else:
                print(f"Директория для '{keyword}' не создана или пуста.")

        print(f"\n Всего реально загружено изображений: {total_downloaded}")

        create_annotation_csv(str(output_dir), args.annotation_file)

        print("\nПример итерации по файлам")
        iterator = FileAnnotationIterator(args.annotation_file)
        for abs_path, rel_path in iterator:
            print(f"Абсолютный путь: {abs_path}")
            print(f"Относительный путь: {rel_path}\n")

        print("Все задачи выполнены успешно!")

    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()