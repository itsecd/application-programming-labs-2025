import argparse
from pathlib import Path
from icrawler.builtin import GoogleImageCrawler


class ImagePathIterator:
    """Итератор по путям к файлам."""
    def __init__(self, annotation_file=None, folder_path=None):
        self.annotation_file = annotation_file
        self.folder_path = folder_path
        if annotation_file is not None and folder_path is not None:
            raise ValueError("Можно задать лишь один аргумент: файл аннотаций ИЛИ путь к папке.")
        
        if annotation_file is not None:
            with open(annotation_file, 'r') as f:
                lines = f.readlines()[1:]  # Пропускаем заголовочную строку
                self.paths = [line.strip() for line in lines]
        elif folder_path is not None:
            folder = Path(folder_path)
            self.paths = [str(p.relative_to(folder)) for p in folder.glob('*')]
        else:
            raise ValueError("Нужно задать хотя бы один аргумент: файл аннотаций или путь к папке.")
    
    def __iter__(self):
        return iter(self.paths)


def download_images(keyword, color, output_dir, max_num=100):
    """
    Скачиваем изображения по запросу и цвету.
    :param keyword: Строка поиска (например, "птица").
    :param color: Цвет изображения ('красный', 'желтый' и т.п.).
    :param output_dir: Директория для сохранения изображений.
    :param max_num: Максимальное число загружаемых изображений.
    """
    google_crawler = GoogleImageCrawler(storage={'root_dir': output_dir})
    filters = dict(color=color.lower())
    google_crawler.crawl(keyword=keyword, filters=filters, max_num=max_num)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Загрузка изображений по ключевому слову и цвету.')
    parser.add_argument('--output-dir', required=True, help='Директория для сохранения изображений')
    parser.add_argument('--annotation-file', help='Файл CSV с путями к изображениям')
    parser.add_argument('--folder-path', help='Путь к папке с изображениями')
    args = parser.parse_args()

    # Создаем каталог для хранения изображений
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Доступные цвета
    colors = ['red', 'yellow', 'green', 'blue']
    print(f"Доступные цвета: {colors}")
    selected_color = input("Выберите цвет изображения: ").strip().lower()
    while selected_color not in colors:
        print("Недопустимый цвет. Попробуйте ещё раз.")
        selected_color = input("Выберите цвет изображения: ").strip().lower()

    # Загружаем изображения птиц выбранного цвета
    download_images('bird', selected_color, str(output_dir))

    # Формируем аннотационный CSV-файл вручную
    with open(str(output_dir / 'annotations.csv'), 'w') as csvfile:
        csvfile.write("absolute_path,relative_path\n")  # Записываем заголовок
        for img_path in sorted(output_dir.iterdir()):
            absolute_path = str(img_path.resolve())
            relative_path = str(img_path.relative_to(output_dir.parent))
            csvfile.write(f"{absolute_path},{relative_path}\n")

    # Используем итератор для обхода путей к файлам
    iterator = ImagePathIterator(annotation_file=str(output_dir / 'annotations.csv'))
    for path in iterator:
        print(path)