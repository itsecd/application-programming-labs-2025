import csv
import os
from pathlib import Path


def create_annotation_csv(image_dir: str, csv_path: str) -> int:
    """Создаёт CSV с метаданными изображений"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
    image_dir_path = Path(image_dir).resolve()
    files_info = []

    for filename in sorted(os.listdir(image_dir)):
        if Path(filename).suffix.lower() in image_extensions:
            abs_path = str(image_dir_path / filename)
            rel_path = os.path.relpath(abs_path, start=os.getcwd())
            files_info.append({
                'filename': filename,
                'absolute_path': abs_path,
                'relative_path': rel_path
            })

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'absolute_path', 'relative_path'])
        writer.writeheader()
        writer.writerows(files_info)

    print(f"Создан CSV с {len(files_info)} записями: {csv_path}")
    return len(files_info)