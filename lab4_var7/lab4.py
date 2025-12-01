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


def add_brightness_range_column(df: pd.DataFrame, bins) -> pd.DataFrame:
    """
    Добавление колонки с диапазонами яркости.
    """

    if bins is None:
        bins = [0, 51, 102, 153, 204, 256]
    
    labels = []
    for i in range(len(bins) - 1):
        labels.append(f"{bins[i]}-{bins[i+1]-1}")

    df['brightness_range'] = pd.cut(df['brightness'], bins=bins, labels=labels, right=False)

    return df, labels


def create_histogram(df: pd.DataFrame, output_path: str, show_plot: bool = False) -> None:
    """
    Построение гистограммы распределения яркости.
    """

    ranges = df['brightness_range'].value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    ranges.plot(kind='bar')

    plt.title('Гистограмма распределения яркости изображений')
    plt.xlabel('Диапазон яркости')
    plt.ylabel('Количество изображений')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(output_path)
    
    if show_plot:
        plt.show()
    else:
        plt.close()


def main() -> None:
    """
    Основная функция программы.
    """
    
    parser = argparse.ArgumentParser(description="Анализ яркости изображений")
    parser.add_argument('--annotation', '-a', required=True,
                       help='Путь к файлу аннотации CSV')
    parser.add_argument('--output_plot', '-op', default='brightness_histogram.png',
                       help='Путь для сохранения гистограммы')
    parser.add_argument('--bins', '-b', nargs='+', type=int, default=[0, 51, 102, 153, 204, 256],
                       help='Границы диапазонов яркости')
    parser.add_argument('--show', action='store_true',
                       help='Показать график')
    
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
        
        # Добавляем диапазоны яркости
        df, brightness_labels = add_brightness_range_column(df, args.bins)
        print(f"Диапазоны яркости: {', '.join(brightness_labels)}")
        
        # Создаем гистограмму
        create_histogram(df, args.output_plot, args.show)
        print(f"Гистограмма сохранена: {args.output_plot}")
        
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()