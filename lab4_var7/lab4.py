# lab4.py
import argparse
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_annotation_data(annotation_path: str) -> pd.DataFrame:
    """
    Загрузка данных из файла аннотации.
    """
    
    try:
        df = pd.read_csv(annotation_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {annotation_path}")
    
    if len(df.columns) >= 2:
        df = df.iloc[:, :2]
        df.columns = ['absolute_path', 'relative_path']
    else:
        raise ValueError("В CSV недостаточно колонок")
    
    return df


def calculate_image_brightness(absolute_path: str) -> float:
    """
    Вычисление средней яркости изображения.
    """

    try:
        image = cv2.imread(absolute_path)
        if image is not None:
            return float(image.mean())
    except Exception:
        pass
    return 0.0


def main() -> None:
    """
    Основная функция программы.
    """
    
    parser = argparse.ArgumentParser(description="Анализ яркости изображений")
    parser.add_argument('--annotation', '-a', required=True,
                       help='Путь к файлу аннотации CSV')
    
    args = parser.parse_args()
    
    try:
        df = load_annotation_data(args.annotation)
        print(f"Загружено изображений: {len(df)}")
        
        # Добавляем колонку с яркостью
        df['brightness'] = df['absolute_path'].apply(calculate_image_brightness)
        
        # Выводим результаты
        failed_count = (df['brightness'] == 0.0).sum()
        print(f"Не удалось обработать изображений: {failed_count}")
        
        df = df[df['brightness'] > 0.0]
        print(f"Успешно обработано изображений: {len(df)}")
        
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()