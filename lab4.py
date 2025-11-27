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
        # Переименовываем колонки для ясности
        df = df.rename(columns={
            'absolute_path': 'absolute_path',
            'relative_path': 'relative_path'
        })
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
