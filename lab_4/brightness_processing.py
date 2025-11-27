"""Модуль для работы с данными и вычислениями."""
import os
import pandas as pd
from PIL import Image
import numpy as np
from ImagePathIterator import ImagePathIterator


def load_image_paths(csv_file: str) -> list:
    """Загрузка путей к изображениям через итератор."""
    if not os.path.exists(csv_file):
        print(f"CSV файл не найден: {csv_file}")
        return []
    
    try:
        iterator = ImagePathIterator(csv_file)

        if len(iterator) == 0:
            print("CSV файл не содержит данных")
            return []

        image_paths=list(iterator)

        print(f"Загружено {len(image_paths)} путей к изображениям")
        return image_paths

    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
        return []


def brightness_range_calculating(image_path: str) -> float:
    """Вычисление диапазона яркости для одного изображения."""
    if not os.path.exists(image_path):
        print(f"{image_path} не существует")
        return None

    try:
        with Image.open(image_path) as img:
            img_array = np.array(img)

        if len(img_array.shape) == 2:
             return float(np.max(img_array) - np.min(img_array))
        else:
             channel_ranges = []
             for channel_num in range(img_array.shape[2]):
                 channel_data = img_array[:, :, channel_num]
                 channel_ranges.append(np.max(channel_data) - np.min(channel_data))

             return float(max(channel_ranges))
             
    except Exception as e:
        print(f"Ошибка при обработке {image_path}: {e}")
        return None


def process_brightness(image_paths: list, original_csv: str) -> pd.DataFrame:
    """Обработка яркости для всех изображений с сохранением исходных данных."""

    original_df = pd.read_csv(original_csv, encoding='utf-8')
    
    results = []
    successful = 0

    for image_path in image_paths:
        brightness = brightness_range_calculating(image_path)

        if brightness is not None:
            original_row = original_df[original_df['Absolute path'] == image_path]
            
            if not original_row.empty:
                result_row = {
                    'Absolute_path': image_path,
                    'Relative_path': original_row['Relative path'].iloc[0],
                    'Keyword': original_row['Keyword'].iloc[0],
                    'Brightness_range': brightness
                }
                results.append(result_row)
                successful += 1

    print(f"Успешно обработано: {successful}/{len(image_paths)} изображений")
    
    if not results:
        return pd.DataFrame()
    
    return pd.DataFrame(results)


def sort_by_brightness(df: pd.DataFrame, ascending: bool = True) -> pd.DataFrame:
    """Сортировка по яркости"""
    return df.sort_values('Brightness_range', ascending=ascending)


def filter_by_brightness(df: pd.DataFrame, min_range: float = None, max_range: float = None) -> pd.DataFrame:
    """Фильтрация диапозона яркости"""
    filtered_df = df.copy()

    if min_range is not None:
        filtered_df = filtered_df[filtered_df['Brightness_range'] >= min_range]
    if max_range is not None:
        filtered_df = filtered_df[filtered_df['Brightness_range'] <= max_range]
        
    return filtered_df
