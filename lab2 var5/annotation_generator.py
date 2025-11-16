
import csv
from pathlib import Path


def create_annotation_csv(output_dir: Path):
    """
    Генерирует аннотационный CSV-файл для сохранённых изображений.
    :param output_dir: Каталог с изображениями.
    """
    with open(str(output_dir / 'annotations.csv'), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["absolute_path", "relative_path"])
        for img_path in sorted(output_dir.iterdir()):
            absolute_path = str(img_path.resolve())
            relative_path = str(img_path.relative_to(output_dir.parent))
            writer.writerow([absolute_path, relative_path])