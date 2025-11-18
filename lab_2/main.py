import argparse
import os
import sys
from ImageDownloader import ImageDownloader
from ImagePathIterator import ImagePathIterator


def main() -> None:
    try:
        parser = argparse.ArgumentParser(description='Скачивание изображений по ключевым словам')
        parser.add_argument('--keywords', '-k', nargs='+', required=True, help='Ключевые слова для поиска изображений')
        parser.add_argument('--save_dir', '-s', required=True, help='Путь к папке для сохранения изображений')
        parser.add_argument('--annotation_file', '-a', required=True, help='Путь к файлу с аннотацией')

        args = parser.parse_args()
    
        print("=" * 50)
        print("ЗАПУСК СКАЧИВАНИЯ ИЗОБРАЖЕНИЙ")
        print("=" * 50)
        print(f"Ключевые слова: {', '.join(args.keywords)}")
        print(f"Директория сохранения: {args.save_dir}")
        print(f"Файл аннотации: {args.annotation_file}")
        print(f"Диапазон изображений на слово: 1-50 (фиксировано)")
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
                    print(f"{i + 1}. {filename}")
        else:
            print("Файлы не найдены")
    
        print("=" * 50)
        print("ПРОГРАММА ЗАВЕРШЕНA")
        print("=" * 50)

    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)
    
   
    


if __name__ == "__main__":
    main()

            