import csv
from pathlib import Path
from typing import List, Union


def create_annotation_csv(image_files: List[Union[str, Path]], output_dir: str, annotation_file: str) -> None:
    """
    Создание CSV файла аннотации
    """
    # Создаем папку для аннотации
    annotation_path = Path(annotation_file)
    annotation_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(annotation_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['absolute_path', 'relative_path'])
        
        output_path = Path(output_dir)
        valid_count = 0
        
        for image_file in image_files:
            img_path = Path(image_file)
            
            if not img_path.exists():
                continue
                
            abs_path = str(img_path.absolute())
            
            # Относительный путь
            try:
                rel_path = str(img_path.relative_to(output_path))
            except ValueError:
                rel_path = str(img_path.name)
            
            writer.writerow([abs_path, rel_path])
            valid_count += 1