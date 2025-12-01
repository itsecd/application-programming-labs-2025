import argparse
import os
import time
from functions import ImageIterator, download_images, create_annotation


def main() -> None:
    """Основная функция программы для скачивания изображений и создания аннотации."""
    try:
        parser = argparse.ArgumentParser(description='Скачать изображения свиней')
        parser.add_argument('--output-dir', required=True, help='Папка для изображений')
        parser.add_argument('--annotation-file', required=True, help='Файл для аннотации')
        parser.add_argument('--timeout', type=int, default=60, help='Время в секундах')
        parser.add_argument('--min-images', type=int, default=50, help='Минимальное количество изображений')
        
        args = parser.parse_args()

        os.makedirs(args.output_dir, exist_ok=True)

        print(f"Скачиваем изображения...")
        print(f"Время: {args.timeout} сек")
        print(f"Минимум изображений: {args.min_images}")

        start_time = time.time()

        download_images(args.output_dir, args.timeout, args.min_images)

        elapsed_time = time.time() - start_time

        create_annotation(args.annotation_file, args.output_dir)

        image_count = len([f for f in os.listdir(args.output_dir) if f.endswith(('.jpg', '.jpeg', '.png'))])

        print(f"\nГотово!")
        print(f"Скачано: {image_count} изображений")
        print(f"Время: {elapsed_time:.1f} сек")
        print(f"Аннотация: {args.annotation_file}")

        print(f"\nИтератор из аннотации:")
        iterator = ImageIterator(annotation_file=args.annotation_file)
        count = 0
        for i, path in enumerate(iterator):
            if i < 3:
                print(f"  {path}")
            count = i + 1
        print(f"Всего путей: {count}")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
