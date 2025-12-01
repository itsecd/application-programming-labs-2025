"""Модуль для работы с данными и вычислениями."""
import os
import pandas as pd
from PIL import Image
import numpy as np
from typing import List, Dict, Tuple, Optional, Union
from ImagePathIterator import ImagePathIterator


def load_image_paths(csv_file: str) -> List[str]:
    """Загрузка путей к изображениям через итератор."""
    if not os.path.exists(csv_file):
        return []
    
    try:
        iterator = ImagePathIterator(csv_file)

        if len(iterator) == 0:
            return []

        image_paths = list(iterator)
        return image_paths

    except Exception:
        return []


def brightness_range_calculating(image_path: str) -> Optional[float]:
    """Вычисление диапазона яркости для одного изображения."""
    if not os.path.exists(image_path):
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
                channel_ranges.append(
                    np.max(channel_data) - np.min(channel_data)
                )

            return float(max(channel_ranges))
             
    except Exception:
        return None


def process_brightness(
    image_paths: List[str], 
    original_csv: str, 
    brightness_ranges: Optional[Dict[str, Tuple[float, float]]] = None
) -> pd.DataFrame:
    """Обработка яркости для всех изображений с сохранением исходных данных."""
    original_df = pd.read_csv(original_csv, encoding='utf-8')
    
    results = []
    successful = 0

    for image_path in image_paths:
        brightness = brightness_range_calculating(image_path)

        if brightness is not None:
            original_row = original_df[
                original_df['Absolute path'] == image_path
            ]
            
            if not original_row.empty:
                brightness_range_label = "Не определено"
                if brightness_ranges:
                    for range_label, (min_val, max_val) in brightness_ranges.items():
                        if min_val <= brightness <= max_val:
                            brightness_range_label = range_label
                            break
                
                result_row = {
                    'Absolute_path': image_path,
                    'Relative_path': original_row['Relative path'].iloc[0],
                    'Keyword': original_row['Keyword'].iloc[0],
                    'Brightness_range': brightness,
                    'Brightness_range_label': brightness_range_label
                }
                results.append(result_row)
                successful += 1

    if not results:
        return pd.DataFrame()
    
    return pd.DataFrame(results)


def sort_by_brightness(
    df: pd.DataFrame, 
    ascending: bool = True
) -> pd.DataFrame:
    """Сортировка по яркости"""
    return df.sort_values('Brightness_range', ascending=ascending)


def filter_by_brightness(
    df: pd.DataFrame, 
    min_range: Optional[float] = None, 
    max_range: Optional[float] = None
) -> pd.DataFrame:
    """Фильтрация диапазона яркости"""
    filtered_df = df.copy()

    if min_range is not None:
        filtered_df = filtered_df[
            filtered_df['Brightness_range'] >= min_range
        ]
    if max_range is not None:
        filtered_df = filtered_df[
            filtered_df['Brightness_range'] <= max_range
        ]
        
    return filtered_df


def create_brightness_ranges(
    ranges_str: str = "0-50,51-100,101-150,151-200,201-255"
) -> Dict[str, Tuple[int, int]]:
    """
    Создание словаря диапазонов яркости из строки.
    
    Args:
        ranges_str: строка в формате "мин-макс,мин-макс,..."
    
    Returns:
        Словарь вида {'0-50': (0, 50), '51-100': (51, 100), ...}
    """
    ranges_dict = {}
    ranges_list = [r.strip() for r in ranges_str.split(',')]
    
    for range_item in ranges_list:
        if '-' in range_item:
            try:
                min_val, max_val = map(int, range_item.split('-'))
                ranges_dict[range_item] = (min_val, max_val)
            except ValueError:
                continue
    
    if not ranges_dict:
        standard_ranges = [
            (0, 50), (51, 100), (101, 150), 
            (151, 200), (201, 255)
        ]
        for min_val, max_val in standard_ranges:
            range_key = f"{min_val}-{max_val}"
            ranges_dict[range_key] = (min_val, max_val)
    
    return ranges_dict