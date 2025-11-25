import csv
from pathlib import Path


def create_annotation(storage_dir: str, annotation_file: str) -> None:
    """Создает CSV файл с путями к изображениям."""
    try:
        storage_path = Path(storage_dir)
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            image_files.extend(storage_path.rglob(ext))
        if not image_files:
            print("No images found for annotation")
            return

        with open(annotation_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            for img_path in image_files:
                abs_path = str(img_path.absolute())
                rel_path = str(img_path.relative_to(storage_path))
                writer.writerow([abs_path, rel_path])

    except Exception as e:
        print(f"Error creating annotation: {e}")