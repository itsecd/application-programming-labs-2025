import os
from pathlib import Path
from typing import List, Tuple

from file_processor import get_file_paths, calculate_brightness_range, create_brightness_range_category
from data_processor import create_dataframe, sort_dataframe, filter_dataframe, get_dataframe_info
from visualizer import plot_histogram
from exporter import save_dataframe, save_plot


def main() -> None:
    """Основная функция программы"""
    # Укажите путь к папке с изображениями
    root_directory = input("Введите путь к папке с изображениями: ").strip()
    
    if not os.path.exists(root_directory):
        print("Указанная папка не существует!")
        return
    
    # Получаем пути к файлам
    print("Сбор информации о файлах...")
    absolute_paths, relative_paths = get_file_paths(root_directory)
    
    if not absolute_paths:
        print("В указанной папке не найдено изображений!")
        return
    
    # Создаем DataFrame с путями и вычисляем яркость
    print(f"Найдено {len(absolute_paths)} изображений")
    print("Вычисление диапазонов яркости...")
    
    df = create_dataframe(absolute_paths, relative_paths)
    
    # Сортируем DataFrame по категориям диапазонов
    print("Сортировка данных...")
    df_sorted = sort_dataframe(df, 'brightness_range_category')
    
    # Фильтрация данных (пример)
    filtered_df = filter_dataframe(df_sorted, 'brightness_range_category', '101-150')
    
    # Вывод информации о данных
    print("\n" + "="*50)
    print("ИНФОРМАЦИЯ О DATAFRAME:")
    print("="*50)
    get_dataframe_info(df_sorted, filtered_df)
    
    # Создаем и сохраняем гистограмму
    print("\nСоздание гистограммы...")
    hist_plot = plot_histogram(df_sorted)
    save_plot(hist_plot, 'brightness_range_histogram.png')
    
    # Сохраняем DataFrame в файлы
    print("Сохранение данных...")
    save_dataframe(df_sorted, 'image_brightness_data')
    
    print("\n" + "="*50)
    print("РЕЗУЛЬТАТЫ СОХРАНЕНЫ:")
    print("="*50)
    print("- image_brightness_data.csv (DataFrame с путями и диапазонами)")
    print("- image_brightness_data.xlsx (Excel версия)")
    print("- brightness_range_histogram.png (гистограмма распределения)")
    
    # Выводим пример данных
    print("\n" + "="*50)
    print("ПРИМЕР ДАННЫХ (первые 3 строки):")
    print("="*50)
    print(df_sorted[['relative_file_path', 'brightness_range_category']].head(3))


if __name__ == "__main__":
    main()