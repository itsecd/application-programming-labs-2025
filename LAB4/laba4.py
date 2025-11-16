import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def get_file_paths(root_dir):
    """Функция для получения абсолютных и относительных путей к файлам"""
    absolute_paths = []
    relative_paths = []
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, root_dir)
                absolute_paths.append(abs_path)
                relative_paths.append(rel_path)
    
    return absolute_paths, relative_paths

def calculate_brightness_range(image_path):
    """Функция для расчета диапазона яркости по каждому каналу (R, G, B)"""
    try:
        with Image.open(image_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img)
            
            # Вычисляем диапазон (max-min) для каждого канала
            r_range = np.max(img_array[:,:,0]) - np.min(img_array[:,:,0])
            g_range = np.max(img_array[:,:,1]) - np.min(img_array[:,:,1])
            b_range = np.max(img_array[:,:,2]) - np.min(img_array[:,:,2])
            
            # Возвращаем максимальный диапазон среди каналов
            return max(r_range, g_range, b_range)
    except Exception as e:
        print(f"Ошибка при обработке {image_path}: {e}")
        return 0

def create_brightness_range_category(brightness_range):
    """Функция для создания категории диапазона яркости"""
    if brightness_range <= 50:
        return "0-50"
    elif brightness_range <= 100:
        return "51-100"
    elif brightness_range <= 150:
        return "101-150"
    elif brightness_range <= 200:
        return "151-200"
    else:
        return "201-255"

def sort_dataframe(df, column='brightness_range_category', ascending=True):
    """Функция сортировки DataFrame по категории диапазона"""
    # Создаем порядок сортировки для категорий
    category_order = ["0-50", "51-100", "101-150", "151-200", "201-255"]
    df['sort_order'] = df[column].apply(lambda x: category_order.index(x))
    df_sorted = df.sort_values('sort_order', ascending=ascending)
    return df_sorted.drop('sort_order', axis=1)

def filter_dataframe(df, column='brightness_range_category', value='101-150'):
    """Функция фильтрации DataFrame"""
    return df[df[column] == value]

def plot_histogram(df):
    """Функция для построения гистограммы распределения по диапазонам"""
    # Подсчет количества файлов в каждой категории
    category_counts = df['brightness_range_category'].value_counts()
    
    # Упорядочиваем категории
    categories_ordered = ["0-50", "51-100", "101-150", "151-200", "201-255"]
    counts_ordered = [category_counts.get(cat, 0) for cat in categories_ordered]
    
    # Создание гистограммы
    plt.figure(figsize=(12, 8))
    
    bars = plt.bar(categories_ordered, counts_ordered, 
                   color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc'],
                   edgecolor='black', alpha=0.7)
    
    # Настройки графика
    plt.title('Гистограмма распределения изображений по диапазонам яркости', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Диапазон яркости', fontsize=12, labelpad=10)
    plt.ylabel('Количество файлов', fontsize=12, labelpad=10)
    plt.grid(axis='y', alpha=0.3)
    
    # Добавление значений на столбцы
    for bar, count in zip(bars, counts_ordered):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{count}', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Улучшаем внешний вид
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    
    return plt

def main():
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
    
    # Создаем DataFrame с путями
    df = pd.DataFrame({
        'absolute_file_path': absolute_paths,
        'relative_file_path': relative_paths
    })
    
    print(f"Найдено {len(df)} изображений")
    print("Вычисление диапазонов яркости...")
    
    # Добавляем колонку с максимальным диапазоном яркости
    df['max_brightness_range'] = [calculate_brightness_range(path) for path in df['absolute_file_path']]
    
    # Добавляем колонку с категорией диапазона (основная колонка для варианта с гистограммой)
    df['brightness_range_category'] = df['max_brightness_range'].apply(create_brightness_range_category)
    
    # Сортируем DataFrame по категориям диапазонов
    print("Сортировка данных...")
    df_sorted = sort_dataframe(df, 'brightness_range_category')
    
    # Фильтрация данных (пример)
    filtered_df = filter_dataframe(df_sorted, 'brightness_range_category', '101-150')
    
    # Вывод информации о данных
    print("\n" + "="*50)
    print("ИНФОРМАЦИЯ О DATAFRAME:")
    print("="*50)
    print(f"Всего изображений: {len(df_sorted)}")
    print(f"Колонки: {list(df_sorted.columns)}")
    print("\nРаспределение по категориям яркости:")
    print(df_sorted['brightness_range_category'].value_counts().sort_index())
    
    print(f"\nФильтрация по категории '101-150': найдено {len(filtered_df)} файлов")
    
    # Создаем и сохраняем гистограмму
    print("\nСоздание гистограммы...")
    hist_plot = plot_histogram(df_sorted)
    hist_plot.savefig('brightness_range_histogram.png', dpi=300, bbox_inches='tight')
    hist_plot.show()
    
    # Сохраняем DataFrame в файлы
    print("Сохранение данных...")
    df_sorted.to_csv('image_brightness_data.csv', index=False, encoding='utf-8')
    df_sorted.to_excel('image_brightness_data.xlsx', index=False)
    
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