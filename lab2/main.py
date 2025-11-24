import argparse
import os
from image_downloader import ImageDownloader
from image_pathIterator import ImagePathIterator


def main() -> None:
    parser = argparse.ArgumentParser(description='Скачивание изображений по ключевым словам')
    parser.add_argument('--keywords', '-k', nargs='+', required=True, 
                       help='Ключевые слова для поиска изображений')
    parser.add_argument('--save_dir', '-s', required=True, 
                       help='Путь к папке для сохранения изображений')
    parser.add_argument('--annotation_file', '-a', required=True, 
                       help='Путь к файлу с аннотацией')

    args = parser.parse_args()

    print("=" * 50)
    print("ЗАПУСК СКАЧИВАНИЯ ИЗОБРАЖЕНИЙ")
    print("=" * 50)
    print(f"Ключевые слова: {', '.join(args.keywords)}")
    print(f"Директория сохранения: {args.save_dir}")
    print(f"Файл аннотации: {args.annotation_file}")
    print("=" * 50)

    downloader = ImageDownloader(keywords=args.keywords)
    total_downloaded = downloader.download_images(args.save_dir)
    downloader.create_annotation(args.save_dir, args.annotation_file)

    print("\n" + "=" * 30)
    print("ДЕМОНСТРАЦИЯ ИТЕРАТОРА")
    print("=" * 30)

    iterator = ImagePathIterator(args.annotation_file)

    print(f"Всего файлов в аннотации: {len(iterator)}")

    if len(iterator) > 0:
        print("Первые 5 файлов:")
        for i, path in enumerate(iterator):
            if i < 5:
                filename = os.path.basename(path)
                keyword = os.path.basename(os.path.dirname(path))
                print(f"{i + 1}. {filename} (класс: {keyword})")
    else:
        print("Файлы не найдены")

    print("=" * 50)
    print("ПРОГРАММА ЗАВЕРШЕНА")
    print("=" * 50)


if __name__ == "__main__":
    main()