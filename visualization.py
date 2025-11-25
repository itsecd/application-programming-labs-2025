"""
Модуль для визуализации данных об амплитудах аудиофайлов.
"""

from typing import Optional
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class AmplitudeVisualizer:
    """Класс для визуализации данных об амплитудах аудиофайлов."""
    
    @staticmethod
    def create_amplitude_plot(df_sorted: pd.DataFrame, 
                             save_path: str = 'audio_amplitude_plot.png') -> None:
        """
        Создает график распределения максимальной амплитуды.
        
        Args:
            df_sorted: Отсортированный DataFrame с данными об амплитудах
            save_path: Путь для сохранения графика
        """
        plt.figure(figsize=(12, 8))
        
        # График для всех отсортированных данных
        x_positions = range(len(df_sorted))
        y_values = df_sorted['Максимальная_амплитуда'].values
        
        plt.plot(x_positions, y_values, 'b-', linewidth=2, alpha=0.7, 
                label='Максимальная амплитуда')
        scatter = plt.scatter(x_positions, y_values, c=y_values, cmap='viridis', 
                             s=50, alpha=0.6)
        
        # Настройки графика
        plt.xlabel('Номер аудиофайла в отсортированном списке', fontsize=12)
        plt.ylabel('Максимальная амплитуда', fontsize=12)
        plt.title('Распределение максимальной амплитуды аудиофайлов', 
                 fontsize=14, fontweight='bold')
        plt.colorbar(scatter, label='Максимальная амплитуда')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Улучшаем читаемость
        plt.tight_layout()
        
        # Сохраняем график
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"График сохранен как '{save_path}'")
        
        # Показываем график
        plt.show()
    
    @staticmethod
    def create_amplitude_histogram(df: pd.DataFrame, 
                                  save_path: str = 'amplitude_distribution.png') -> None:
        """
        Создает гистограмму распределения амплитуд.
        
        Args:
            df: DataFrame с данными об амплитудах
            save_path: Путь для сохранения гистограммы
        """
        plt.figure(figsize=(10, 6))
        plt.hist(df['Максимальная_амплитуда'], bins=20, alpha=0.7, 
                color='skyblue', edgecolor='black')
        plt.xlabel('Максимальная амплитуда')
        plt.ylabel('Количество файлов')
        plt.title('Распределение максимальных амплитуд аудиофайлов')
        plt.grid(True, alpha=0.3)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Гистограмма сохранена как '{save_path}'")