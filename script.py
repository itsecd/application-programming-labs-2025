import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os
import sys


def calculate_brightness_range(image_path):
    """Вычисляет диапазон яркости изображения (max-min) по всем каналам."""
    try:
        img = Image.open(image_path)
        img_array = np.array(img)
        brightness_range = img_array.max() - img_array.min()
        return brightness_range
    except Exception as e:
        print(f"Ошибка при обработке {image_path}: {e}")
        return None


def sort_by_brightness_range(dataframe, ascending=True):
    """Сортировка DataFrame по колонке 'brightness_range'."""
    return dataframe.sort_values('brightness_range', ascending=ascending)


def filter_by_brightness_range(dataframe, min_value=None, max_value=None):
    """Фильтрация DataFrame по диапазону яркости."""
    filtered_df = dataframe.copy()
    if min_value is not None:
        filtered_df = filtered_df[filtered_df['brightness_range'] >= min_value]
    if max_value is not None:
        filtered_df = filtered_df[filtered_df['brightness_range'] <= max_value]
    return filtered_df


def main():
    if len(sys.argv) != 2:
        print("Использование: python script.py <input_csv_file>")
        print("Пример: python script.py annotation.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # 1. Загрузка данных и формирование DataFrame
    if not os.path.exists(input_file):
        print(f"Ошибка: Файл {input_file} не найден!")
        sys.exit(1)
    
    print("=" * 60)
    print("1. ЗАГРУЗКА ДАННЫХ И ФОРМИРОВАНИЕ DATAFRAME")
    print("=" * 60)
    
    df = pd.read_csv(input_file)
    print("Исходный DataFrame:")
    print(df.head())
    print(f"\nРазмер DataFrame: {df.shape}")
    print(f"Колонки: {list(df.columns)}")
    
    # 2. Переименование колонок - оставляем английские названия
    print("\n" + "=" * 60)
    print("2. ПЕРЕИМЕНОВАНИЕ КОЛОНОК")
    print("=" * 60)
    
    print("DataFrame c понятными названиями")
    print(df.head())
    print(f"Названия колонок: {list(df.columns)}")
    
    # 3. Добавление новой колонки
    print("\n" + "=" * 60)
    print("3. ДОБАВЛЕНИЕ КОЛОНКИ С ДИАПАЗОНОМ ЯРКОСТИ")
    print("=" * 60)
    
    print("Вычисление диапазона яркости для изображений...")
    df['brightness_range'] = df['absolute_path'].apply(calculate_brightness_range)
    
    # Удаляем строки с ошибками загрузки изображений
    initial_count = len(df)
    df = df.dropna(subset=['brightness_range'])
    final_count = len(df)
    
    if initial_count != final_count:
        print(f"Предупреждение: {initial_count - final_count} изображений не удалось обработать")
    
    print("\nDataFrame с новой колонкой:")
    print(df.head(10))
    print(f"\nСтатистика по колонке 'brightness_range':")
    print(df['brightness_range'].describe())
    
    # 4. Сортировка по добавленной колонке
    print("\n" + "=" * 60)
    print("4. СОРТИРОВКА ПО КОЛОНКЕ 'brightness_range'")
    print("=" * 60)
    
    sorted_df = sort_by_brightness_range(df)
    print("Первые 10 строк после сортировки (по возрастанию):")
    print(sorted_df[['relative_path', 'brightness_range']].head(10))
    
    # 5. Демонстрация фильтрации
    print("\n" + "=" * 60)
    print("5. ФИЛЬТРАЦИЯ ПО ДИАПАЗОНУ ЯРКОСТИ")
    print("=" * 60)
    
    # Фильтрация с высокой контрастностью
    high_contrast = filter_by_brightness_range(df, min_value=200)
    print(f"Изображения с высокой контрастностью (яркость >= 200): {len(high_contrast)}")
    
    # 6. Построение графика для всех отсортированных данных
    print("\n" + "=" * 60)
    print("6. ПОСТРОЕНИЕ ГРАФИКА ДЛЯ ОТСОРТИРОВАННЫХ ДАННЫХ")
    print("=" * 60)
    
    plt.figure(figsize=(14, 8))
    
    plt.plot(
        range(len(sorted_df)), 
        sorted_df['brightness_range'], 
        marker='o', 
        linewidth=1.5, 
        markersize=3,
        color='blue',
        alpha=0.7,
        label='Диапазон яркости'
    )
    
    plt.xlabel('Порядковый номер изображения в отсортированном списке', fontsize=12)
    plt.ylabel('Диапазон яркости (max-min)', fontsize=12)
    plt.title('Зависимость диапазона яркости от порядка в отсортированном списке', fontsize=14, fontweight='bold')
    
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)

    plt.tight_layout()
    
    output_plot = 'brightness_range_sorted_plot.png'
    plt.savefig(output_plot, dpi=300, bbox_inches='tight')
    print(f"График сохранен в файл: {output_plot}")
    
    plt.show()
    
    # 7. Сохранение DataFrame в файл
    print("\n" + "=" * 60)
    print("7. СОХРАНЕНИЕ DATAFRAME В ФАЙЛ")
    print("=" * 60)
    
    output_csv = 'result_dataframe.csv'
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"DataFrame сохранен в файл: {output_csv}")
    
    # Итоговая информация
    print("\n" + "=" * 60)
    print("ИТОГОВАЯ ИНФОРМАЦИЯ")
    print("=" * 60)
    print(f"Обработано изображений: {len(df)}")
    print(f"Диапазон яркости: от {df['brightness_range'].min():.2f} до {df['brightness_range'].max():.2f}")
    print(f"Средний диапазон яркости: {df['brightness_range'].mean():.2f}")
    
    print(f"\nСохраненные файлы:")
    print(f"- DataFrame: {output_csv}")
    print(f"- График: {output_plot}")
    
    """# Дополнительная информация о сортировке
    print("\n" + "=" * 60)
    print("ИНФОРМАЦИЯ О СОРТИРОВКЕ")
    print("=" * 60)
    print("Первые 5 изображений с наименьшим диапазоном яркости:")
    print(sort_by_brightness_range(df, ascending=True)[['relative_path', 'brightness_range']].head())
    
    print("\nПервые 5 изображений с наибольшим диапазоном яркости:")
    print(sort_by_brightness_range(df, ascending=False)[['relative_path', 'brightness_range']].head())
"""

if __name__ == "__main__":
    main()