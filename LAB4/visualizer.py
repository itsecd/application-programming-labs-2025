import matplotlib.pyplot as plt
import pandas as pd
from typing import List


def plot_histogram(df: pd.DataFrame) -> plt.Figure:
    """
    Функция для построения гистограммы распределения по диапазонам
    
    Args:
        df: DataFrame с данными
        
    Returns:
        Объект Figure matplotlib
    """
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
    
    return plt.gcf()