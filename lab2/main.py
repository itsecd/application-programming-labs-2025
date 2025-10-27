import argparse
from pathlib import Path

from date_parser import parse_date_ranges
from image_distributor import ImageDistributor
from image_downloader import BearImageDownloader
from annotation_creator import create_annotation_csv
from image_iterator import ImageIterator


def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(description='Скачивание изображений медведей')
    parser.add_argument('--output_dir', required=True, help='Папка для изображений')
    parser.add_argument('--annotation_file', required=True, help='Файл аннотации')
    parser.add_argument('--date_ranges', required=True, help='Диапазоны дат')

    args = parser.parse_args()

    try:
        # Парсим даты
        date_ranges = parse_date_ranges(args.date_ranges)
        print(f"Найдено диапазонов: {len(date_ranges)}")

        # Распределяем изображения
        distributor = ImageDistributor()
        total_images, images_per_range = distributor.distribute_with_user_input(len(date_ranges))

        # Скачиваем
        downloader = BearImageDownloader()
        image_paths = downloader.download_images(date_ranges, images_per_range, args.output_dir)

        # Создаем аннотацию
        create_annotation_csv(image_paths, args.annotation_file, args.output_dir)

        # Показываем результат
        print(f"\nФИНАЛЬНЫЙ РЕЗУЛЬТАТ: {len(image_paths)} изображений")

        # Демонстрируем итератор
        print("\nДемонстрация итератора (первые 3 файла):")
        iterator = ImageIterator(args.annotation_file)
        for i, path in enumerate(iterator):
            if i < 3:
                print(f"  {Path(path).name}")
            else:
                break

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()