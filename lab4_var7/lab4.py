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


def add_brightness_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавление колонки с яркостью изображений.
    """

    df['brightness'] = df['absolute_path'].apply(calculate_image_brightness)
    
    failed_count = (df['brightness'] == 0.0).sum()
    if failed_count > 0:
        print(f"Не удалось обработать изображений: {failed_count}")
    
    df = df[df['brightness'] > 0.0]

    return df


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


def sort_by_brightness(df: pd.DataFrame) -> pd.DataFrame:
    """
    Сортировка DataFrame по яркости.
    """

    return df.sort_values(by="brightness", ascending=True)


def filter_by_brightness_range(df: pd.DataFrame, brightness_range: str) -> pd.DataFrame:
    """
    Фильтрация DataFrame по диапазону яркости.
    """

    mask = df['brightness_range'] == brightness_range
    return df[mask]


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


def save_dataframe(df: pd.DataFrame, output_csv_path: str) -> None:
    """
    Сохранение DataFrame в CSV файл.
    """

    df.to_csv(output_csv_path, index=False)


def parse_arguments():
    """
    Парсинг аргументов командной строки.
    """

    parser = argparse.ArgumentParser(description="Анализ яркости изображений")
    
    parser.add_argument('--annotation', '-a', required=True,
                       help='Путь к файлу аннотации CSV')
    
    parser.add_argument('--output_csv', '-oc', default='analysis_results.csv',
                       help='Путь для сохранения результатов в CSV')
    
    parser.add_argument('--output_plot', '-op', default='brightness_histogram.png',
                       help='Путь для сохранения гистограммы')
    
    parser.add_argument('--bins', '-b', nargs='+', type=int, default=[0, 51, 102, 153, 204, 256],
                       help='Границы диапазонов яркости')
    
    parser.add_argument('--filter_range', '-f',
                       help='Диапазон для фильтрации')
    
    parser.add_argument('--show', action='store_true',
                       help='Показать график')

    return parser.parse_args()


def main() -> None:
    """
    Основная функция программы.
    """

    args = parse_arguments()
    
    try:
        df = load_annotation_data(args.annotation)
        print(f"Загружено изображений: {len(df)}")

        df = add_brightness_column(df)
        print(f"Успешно обработано изображений: {len(df)}")

        df, brightness_labels = add_brightness_range_column(df, args.bins)
        print(f"Диапазоны яркости: {', '.join(brightness_labels)}")

        df_sorted = sort_by_brightness(df)

        if args.filter_range:
            if args.filter_range in brightness_labels:
                df_filtered = filter_by_brightness_range(df_sorted, args.filter_range)
                print(f"\nРезультат фильтрации по диапазону '{args.filter_range}':")
                print(f"Найдено изображений: {len(df_filtered)}")
                if len(df_filtered) > 0:
                    print(df_filtered[['relative_path', 'brightness', 'brightness_range']].head())
            else:
                print(f"\nДиапазон '{args.filter_range}' не найден")
                print(f"Доступные диапазоны: {', '.join(brightness_labels)}")

        create_histogram(df_sorted, args.output_plot, args.show)
        print(f"Гистограмма сохранена: {args.output_plot}")

        save_dataframe(df_sorted, args.output_csv)
        print(f"Результаты сохранены в CSV: {args.output_csv}")
        
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()