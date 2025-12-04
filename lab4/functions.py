import pandas as pd
from PIL import Image
from typing import List
import matplotlib.pyplot as plt

def read_annotation_file(annotation_file: str) -> pd.DataFrame:
    """Читает файл аннотации CSV и возвращает DataFrame.
    
    Args:
        annotation_file: Путь к файлу аннотации CSV.
        
    Returns:
        pd.DataFrame: DataFrame с данными из файла аннотации.
        
    Raises:
        Exception: Если возникает ошибка при чтении файла.
    """
    
    try:
        df = pd.read_csv(annotation_file)
        return df
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла аннотации: {e}")

def calculate_aspect_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """Рассчитывает соотношения сторон для изображений в DataFrame.
    
    Args:
        df: DataFrame с путями к изображениям в колонке 'absolute_path'.
        
    Returns:
        pd.DataFrame: DataFrame с добавленной колонкой 'aspect_ratio'.
        
    Raises:
        Exception: Если возникает ошибка при расчете соотношений сторон.
    """
    
    try:
        aspect_ratios = []
        for path in df['absolute_path']:
            try:
                with Image.open(path) as img:
                    width, height = img.size
                    aspect_ratios.append(round(width / height, 2))
            except Exception as e:
                aspect_ratios.append(1.33)  # значение по умолчанию

        df['aspect_ratio'] = aspect_ratios
        return df
    except Exception as e:
        raise Exception(f"Ошибка при расчете соотношений сторон: {e}")

def add_range_column(df: pd.DataFrame, bins: List[float]) -> pd.DataFrame:
    """Добавляет колонку с диапазонами соотношений сторон.
    
    Args:
        df: DataFrame с колонкой 'aspect_ratio'.
        bins: Список границ диапазонов.
        
    Returns:
        pd.DataFrame: DataFrame с добавленной колонкой 'range'.
        
    Raises:
        Exception: Если возникает ошибка при добавлении столбца диапазонов.
    """
    
    try:
        labels = [f'{bins[i]}-{bins[i+1]}' for i in range(len(bins)-1)]
        df['range'] = pd.cut(df['aspect_ratio'], bins=bins, labels=labels)
        return df
    except Exception as e:
        raise Exception(f"Ошибка при добавлении столбца диапазонов: {e}")

def sort_by_aspect_ratio(df: pd.DataFrame) -> pd.DataFrame:
    """Сортирует DataFrame по соотношению сторон.
    
    Args:
        df: DataFrame с колонкой 'aspect_ratio'.
        
    Returns:
        pd.DataFrame: Отсортированный DataFrame.
        
    Raises:
        Exception: Если возникает ошибка при сортировке.
    """
    
    try:
        return df.sort_values('aspect_ratio')
    except Exception as e:
        raise Exception(f"Ошибка при сортировке: {e}")

def filter_by_range(df: pd.DataFrame, range_filter: str) -> pd.DataFrame:
    """Фильтрует DataFrame по указанному диапазону соотношений сторон.
    
    Args:
        df: DataFrame с колонкой 'range'.
        range_filter: Диапазон для фильтрации (например: '1.0-1.5').
        
    Returns:
        pd.DataFrame: Отфильтрованный DataFrame.
        
    Raises:
        Exception: Если возникает ошибка при фильтрации.
    """
    
    try:
        return df[df['range'] == range_filter]
    except Exception as e:
        raise Exception(f"Ошибка при фильтрации: {e}")

def create_histogram(df: pd.DataFrame, filename: str = 'histogram.png') -> None:
    """Создает и сохраняет гистограмму распределения соотношений сторон.
    
    Args:
        df: DataFrame с колонкой 'range'.
        filename: Имя файла для сохранения гистограммы.
    """
    
    plt.figure(figsize=(8, 5))
    df['range'].value_counts().sort_index().plot(kind='bar')
    plt.title('Распределение по соотношению сторон')
    plt.xlabel('Диапазон соотношения')
    plt.ylabel('Количество изображений')
    plt.savefig(filename)
    plt.show()
