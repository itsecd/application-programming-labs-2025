import argparse
from pathlib import Path
from typing import List, Optional, Iterator
from icrawler.builtin import GoogleImageCrawler


def download_images(keyword: str, color: str, output_dir: Path, max_num: int = 100) -> None:
    """
    Скачивает изображения по запросу и цвету.
    :param keyword: Строка поиска (например, "птица").
    :param color: Цвет изображения ('красный', 'желтый' и т.п.).
    :param output_dir: Директория для сохранения изображений.
    :param max_num: Максимальное количество загружаемых изображений.
    """
    google_crawler = GoogleImageCrawler(storage={"root_dir": str(output_dir)})
    filters = {"color": color.lower()}
    google_crawler.crawl(keyword=keyword, filters=filters, max_num=max_num)


class ImagePathIterator:
    """Итератор по путям к файлам."""
    def __init__(self, annotation_file: Optional[str], folder_path: Optional[str]) -> None:
        self.annotation_file = annotation_file
        self.folder_path = folder_path
        if annotation_file is not None and folder_path is not None:
            raise ValueError("Можно задать лишь один аргумент: файл аннотаций ИЛИ путь к папке.")
        
        if annotation_file is not None:
            with open(annotation_file, 'r') as f:
                lines = f.readlines()[1:]  
                self.paths = [line.strip() for line in lines]
        elif folder_path is not None:
            folder = Path(folder_path)
            self.paths = [str(p.relative_to(folder)) for p in folder.glob('*')]
        else:
            raise ValueError("Нужно задать хотя бы один аргумент: файл аннотаций или путь к папке.")
    
    def __iter__(self) -> Iterator[str]:
        return iter(self.paths)


def create_annotation_csv(output_dir: Path) -> None:
    """
    Генерирует аннотационный CSV-файл для сохраненных изображений.
    :param output_dir: Каталог с изображениями.
    """
    with open(str(output_dir / 'annotations.csv'), 'w') as csvfile:
        csvfile.write("absolute_path,relative_path\n")  
        for img_path in sorted(output_dir.iterdir()):
            absolute_path = str(img_path.resolve())
            relative_path = str(img_path.relative_to(output_dir.parent))
            csvfile.write(f"{absolute_path},{relative_path}\n")



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

    google_crawler = GoogleImageCrawler(storage={"root_dir": str(output_dir)}, delay=1)
    iterator = ImagePathIterator(annotation_file=str(output_dir / 'annotations.csv'))
    for path in iterator:
        print(path)


if __name__ == "__main__":
    main()