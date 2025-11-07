import argparse
from pathlib import Path

from image_crawler.core import download_images, create_annotation_csv
from image_crawler.iterators import ImagePathIterator


def main() -> None:
    """CLI-интерфейс для скачивания и аннотации изображений."""
    parser = argparse.ArgumentParser(description='Скачивание изображений через icrawler')
    parser.add_argument('--keyword', type=str, default='cat', help='Ключевое слово поиска')
    parser.add_argument('--num_images', type=int, default=50, help='Количество изображений (50–1000)')
    parser.add_argument('--min_size', type=int, nargs=2, default=[200, 200], metavar=('W', 'H'))
    parser.add_argument('--max_size', type=int, nargs=2, default=[5000, 5000], metavar=('W', 'H'))
    parser.add_argument('--save_dir', type=str, default='./images', help='Папка для сохранения')
    parser.add_argument('--csv_path', type=str, default='./annotation.csv', help='Путь к CSV аннотации')
    args = parser.parse_args()

    if not (50 <= args.num_images <= 1000):
        print("Ошибка: количество изображений должно быть от 50 до 1000")
        return

    download_images(args.keyword, args.num_images, tuple(args.min_size), tuple(args.max_size), args.save_dir)
    total = create_annotation_csv(args.save_dir, args.csv_path)

    print(f"\nСоздан CSV: {args.csv_path}, файлов: {total}")

    print("\nДемонстрация итератора:")
    iterator = ImagePathIterator(args.save_dir)
    for i, path in enumerate(iterator):
        if i >= 5:
            break
        print(f"{i+1}. {Path(path).name}")

    print("\nЗавершено успешно.")


if __name__ == '__main__':
    main()
