import argparse
import os
import time
from functions import ImageIterator, download_images, create_annotation


def main():
    try:
        # Парсим аргументы командной строки
        parser = argparse.ArgumentParser(description='Скачать изображения свиней')
        parser.add_argument('--output-dir', required=True, help='Папка для изображений')
        parser.add_argument('--annotation-file', required=True, help='Файл для аннотации')
        parser.add_argument('--timeout', type=int, required=True, help='Время в секундах')
        
        args = parser.parse_args()

        # Создаем папку если нет
        os.makedirs(args.output_dir, exist_ok=True)

        print(f"Скачиваем изображения 'pig'...")
        print(f"Время: {args.timeout} сек")
        print(f"Папка: {args.output_dir}")

        # Засекаем время
        start_time = time.time()

        # Скачиваем изображения
        download_images(args.output_dir)

        # Считаем время
        elapsed_time = time.time() - start_time

        # Создаем CSV аннотацию
        create_annotation(args.annotation_file, args.output_dir)

        # Считаем сколько скачали
        image_count = len([f for f in os.listdir(args.output_dir) if f.endswith(('.jpg', '.jpeg', '.png'))])

        # Выводим результаты
        print(f"\nГотово!")
        print(f"Скачано: {image_count} изображений")
        print(f"Время: {elapsed_time:.1f} сек")
        print(f"Аннотация: {args.annotation_file}")

        #работа итератора
        print(f"\nИтератор из аннотации:")
        iterator = ImageIterator(annotation_file=args.annotation_file)
        for i, path in enumerate(iterator):
            if i < 3:  # Показываем первые 3 пути
                print(f"  {path}")
        print(f"Всего путей: {i + 1}")

    except Exception as e:
        print(f"Критическая ошибка: {e}")


if __name__ == "__main__":
    main()