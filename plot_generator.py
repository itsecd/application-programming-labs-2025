"""Модуль для генерации графиков."""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import config


class PlotGenerator:
    """Класс для генерации графиков из аудиоданных."""
    
    def __init__(self) -> None:
        """Инициализация генератора графиков с применением стиля seaborn."""
        plt.style.use('seaborn-v0_8')
    
    def create_amplitude_histogram(self, df: pd.DataFrame, output_file: Path) -> None:
        """Создает гистограмму распределения файлов по диапазонам амплитуды."""
        try:
            plt.figure(figsize=(10, 6))
            
            range_counts = df['amplitude_range_bin'].value_counts().sort_index()
            plt.bar(range(len(range_counts)), range_counts.values, color='skyblue')
            plt.xlabel('Диапазоны амплитуды')
            plt.ylabel('Количество файлов')
            plt.title('Распределение файлов по диапазонам амплитуды')
            plt.xticks(range(len(range_counts)), range_counts.index, rotation=45)
            
            plt.tight_layout()
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            print(f"Ошибка при создании гистограммы: {e}")
            raise
    
    def create_sorted_amplitude_plot(self, df: pd.DataFrame, output_file: Path) -> None:
        """Создает график отсортированных значений амплитуды."""
        try:
            plt.figure(figsize=(10, 6))
            plt.plot(range(len(df)), df['amplitude_range'], marker='o', markersize=2)
            plt.xlabel('Номер файла в отсортированном списке')
            plt.ylabel('Диапазон амплитуды')
            plt.title('Отсортированные значения амплитуды')
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            print(f"Ошибка при создании графика: {e}")
            raise