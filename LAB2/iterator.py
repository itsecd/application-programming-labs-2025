import csv
import os
from pathlib import Path
from typing import List, Optional, Union


class ImageDatasetIterator:
    """Итератор по путям к файлам изображений"""
    
    def __init__(self, annotation_file: Optional[str] = None, folder_path: Optional[str] = None) -> None:
        if annotation_file:
            self.paths = self._load_from_annotation(annotation_file)
        elif folder_path:
            self.paths = self._load_from_folder(folder_path)
        else:
            raise ValueError("Необходимо указать либо annotation_file, либо folder_path")
        
        self.index = 0
    
    def _load_from_annotation(self, annotation_file: str) -> List[str]:
        """Загрузка путей из CSV файла аннотации"""
        paths: List[str] = []
        
        if not os.path.exists(annotation_file):
            return paths
            
        try:
            with open(annotation_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if 'absolute_path' in row and os.path.exists(row['absolute_path']):
                        paths.append(row['absolute_path'])
        except Exception:
            pass
        return paths
    
    def _load_from_folder(self, folder_path: str) -> List[str]:
        """Загрузка путей из папки"""
        paths: List[str] = []
        
        if not os.path.exists(folder_path):
            return paths
            
        try:
            folder = Path(folder_path)
            # Ищем все файлы с изображениями
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.webp']:
                paths.extend([str(p) for p in folder.rglob(ext)])
                paths.extend([str(p) for p in folder.rglob(ext.upper())])
            
            # Убираем дубликаты
            paths = list(set(paths))
        except Exception:
            pass
        
        return paths
    
    def __iter__(self) -> 'ImageDatasetIterator':
        self.index = 0
        return self
    
    def __next__(self) -> str:
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        else:
            raise StopIteration
    
    def __len__(self) -> int:
        return len(self.paths)