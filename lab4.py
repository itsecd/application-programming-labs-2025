import argparse
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os
import numpy as np

def create_dataframe_from_annotation(annotation_file):
    """
    Создает DataFrame из файла аннотации
    
    Args:
        annotation_file (str): Путь к CSV файлу аннотации
    
    Returns:
        pd.DataFrame: DataFrame с путями к файлам
    """
    try:
        df = pd.read_csv(annotation_file)
        return df
    except Exception as e:
        print(f"Ошибка чтения аннотации: {e}")
        return None

def create_dataframe_from_folder(folder_path):
    """
    Создает DataFrame из папки с изображениями
    
    Args:
        folder_path (str): Путь к папке с изображениями
    
    Returns:
        pd.DataFrame: DataFrame с путями к файлам
    """
    try:
        data = []
        parent_dir = os.path.abspath(os.path.join(folder_path, os.pardir))
        
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                absolute_path = os.path.abspath(file_path)
                relative_path = os.path.relpath(absolute_path, parent_dir)
                
                data.append({
                    'absolute_path': absolute_path,
                    'relative_path': relative_path
                })
        
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Ошибка создания DataFrame из папки: {e}")
        return None

def add_aspect_ratio_column(df):
    """
    Добавляет колонку с отношением сторон изображения
    
    Args:
        df (pd.DataFrame): Исходный DataFrame
    
    Returns:
        pd.DataFrame: DataFrame с добавленной колонкой aspect_ratio
    """
    aspect_ratios = []
    
    for idx, row in df.iterrows():
        try:
            with Image.open(row['absolute_path']) as img:
                width, height = img.size
                # ширина к высоте
                aspect_ratio = round(width / height, 2)
                aspect_ratios.append(aspect_ratio)
        except Exception as e:
            print(f"Ошибка обработки {row['absolute_path']}: {e}")
            aspect_ratios.append(None)
    
    df['aspect_ratio'] = aspect_ratios
    return df

def add_aspect_ratio_bins_column(df, bins=5):
    """
    Добавляет колонку с диапазонами отношений сторон для гистограммы
    
    Args:
        df (pd.DataFrame): DataFrame с колонкой aspect_ratio
        bins (int): Количество диапазонов
    
    Returns:
        pd.DataFrame: DataFrame с добавленной колонкой aspect_ratio_range
    """
    # Удаляем NaN
    df_clean = df.dropna(subset=['aspect_ratio'])
    
    if len(df_clean) == 0:
        print("Нет данных для создания диапазонов")
        return df
    
    # диапазоны
    min_ratio = df_clean['aspect_ratio'].min()
    max_ratio = df_clean['aspect_ratio'].max()
    
    # границы
    boundaries = np.linspace(min_ratio, max_ratio, bins + 1)
    
    # определение диапазона
    def get_ratio_range(ratio):
        for i in range(len(boundaries) - 1):
            if boundaries[i] <= ratio <= boundaries[i + 1]:
                return f"{boundaries[i]:.2f}-{boundaries[i + 1]:.2f}"
        return "Unknown"
    
    df['aspect_ratio_range'] = df['aspect_ratio'].apply(
        lambda x: get_ratio_range(x) if pd.notnull(x) else "Unknown"
    )
    
    return df
