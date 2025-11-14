
import argparse
from pathlib import Path
from image_downloader import download_images
from annotation_generator import create_annotation_csv
from path_iterator import ImagePathIterator


def main():
    parser = argparse.ArgumentParser(description='Загрузка изображений по ключевому слову и цвету.')
    parser.add_argument('--output-dir', required=True, help='Директория для сохранения изображений')
    parser.add_argument('--keyword', default='bird', help='Ключевое слово для поиска изображений')
    parser.add_argument('--color', choices=['red', 'yellow', 'green', 'blue'], required=True, help='Цвет изображения')
    parser.add_argument('--annotation-file', help='Файл CSV с путями к изображениям')
    parser.add_argument('--folder-path', help='Путь к папке с изображениями')
    args = parser.parse_args()

   
    output_dir = Path(args.output_dir) / f"{args.keyword}_{args.color}"
    output_dir.mkdir(parents=True, exist_ok=True)

    
    download_images(args.keyword, args.color, output_dir)

    
    create_annotation_csv(output_dir)

    
    iterator = ImagePathIterator(annotation_file=str(output_dir / 'annotations.csv'))
    for path in iterator:
        print(path)


if __name__ == "__main__":
    main()