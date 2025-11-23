import os
import csv
from pathlib import Path
from typing import Union
from icrawler.builtin import BingImageCrawler


def download_images(
    output_dir: Union[str, Path],
    annotation_file: Union[str, Path],
    num_threads: int,
    keyword: str = "cow",
    max_num: int = 1000
) -> None:
    """Скачивает изображения и создает CSV-аннотацию.
    
    Args:
        output_dir: Директория для сохранения изображений
        annotation_file: Путь для создания CSV-аннотации
        num_threads: Количество потоков скачивания
        keyword: Ключевое слово для поиска "cow"
        max_num: Максимальное количество изображений 1000
    
    Raises:
        Exception: Если произошла ошибка при скачивании изображений
    """
    output_dir = Path(output_dir)
    annotation_file = Path(annotation_file)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    annotation_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        crawler = BingImageCrawler(
            storage={'root_dir': str(output_dir)},
            downloader_threads=num_threads
        )
        crawler.crawl(keyword=keyword, max_num=max_num)
        
        _create_annotation(output_dir, annotation_file)
        print(f"Успешно скачано изображений в {output_dir}")
        print(f"Аннотация создана в {annotation_file}")
        
    except Exception as e:
        print(f"Ошибка при скачивании изображений: {e}")
        raise


def _create_annotation(output_dir: Path, annotation_file: Path) -> None:
    """Создает CSV-файл аннотации с путями к изображениям.
    
    Args:
        output_dir: Директория с изображениями
        annotation_file: Путь к файлу аннотации
    """
    with open(annotation_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['absolute_path', 'relative_path', 'filename']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for root, _, files in os.walk(output_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    abs_path = os.path.abspath(os.path.join(root, file))
                    rel_path = os.path.relpath(abs_path, start=annotation_file.parent)
                    writer.writerow({
                        'absolute_path': abs_path,
                        'relative_path': rel_path,
                        'filename': file
                    })