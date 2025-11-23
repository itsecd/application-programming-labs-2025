import pandas as pd
from PIL import Image
from typing import List

def read_annotation_file(annotation_file: str) -> pd.DataFrame:
    
    try:
        df = pd.read_csv(annotation_file)
        return df
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла аннотации: {e}")

def calculate_aspect_ratios(df: pd.DataFrame) -> pd.DataFrame:
    
    try:
        aspect_ratios = []
        for path in df['Абсолютный путь']:
            try:
                with Image.open(path) as img:
                    width, height = img.size
                    aspect_ratios.append(round(width / height, 2))
            except Exception as e:
                print(f"Ошибка при обработке изображения {path}: {e}")
                aspect_ratios.append(1.33)  # значение по умолчанию

        df['aspect_ratio'] = aspect_ratios
        return df
    except Exception as e:
        raise Exception(f"Ошибка при расчете соотношений сторон: {e}")

def add_range_column(df: pd.DataFrame, bins: List[float]) -> pd.DataFrame:
    
    try:
        labels = [f'{bins[i]}-{bins[i+1]}' for i in range(len(bins)-1)]
        df['range'] = pd.cut(df['aspect_ratio'], bins=bins, labels=labels)
        return df
    except Exception as e:
        raise Exception(f"Ошибка при добавлении столбца диапазонов: {e}")

def sort_by_aspect_ratio(df: pd.DataFrame) -> pd.DataFrame:
    
    try:
        return df.sort_values('aspect_ratio')
    except Exception as e:
        raise Exception(f"Ошибка при сортировке: {e}")

def filter_by_range(df: pd.DataFrame, range_filter: str) -> pd.DataFrame:
    
    try:
        return df[df['range'] == range_filter]
    except Exception as e:

        raise Exception(f"Ошибка при фильтрации: {e}")
