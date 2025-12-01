"""Модуль для генерации графиков с помощью matplotlib."""
import os

import matplotlib.pyplot as plt
import pandas as pd

class PlotGenerator:
    """Класс для генерации графиков анализа аудиофайлов."""

    @staticmethod
    def create_duration_plot(sorted_df: pd.DataFrame, output_path: str) -> None:
        """
        Создает график длительности аудиофайлов для отсортированных данных.

        Args:
            sorted_df: Отсортированный DataFrame с данными об аудиофайлах
            output_path: Путь для сохранения графика

        Raises:
            ValueError: Если DataFrame не содержит необходимые колонки
            Exception: Если произошла ошибка при создании графика
        """
        if 'duration_seconds' not in sorted_df.columns:
            raise ValueError("DataFrame не содержит колонку 'duration_seconds'")

        try:
            sorted_df_reset = sorted_df.reset_index(drop=True)
            
            plt.figure(figsize=(12, 6))
            plt.plot(sorted_df_reset.index, sorted_df_reset['duration_seconds'], 
                    marker='o', linewidth=2, markersize=4, alpha=0.7, color='blue')
            
            plt.title('Распределение длительности аудиофайлов (отсортировано по возрастанию)', 
                     fontsize=14, fontweight='bold')
            plt.xlabel('Порядковый номер файла в отсортированном списке', fontsize=12)
            plt.ylabel('Длительность (секунды)', fontsize=12)
            plt.grid(True, alpha=0.3)
            
            total_files = len(sorted_df_reset)
            min_duration = sorted_df_reset['duration_seconds'].min()
            max_duration = sorted_df_reset['duration_seconds'].max()
            plt.text(0.02, 0.98, f'Всего файлов: {total_files}\nМин: {min_duration}с, Макс: {max_duration}с', 
                    transform=plt.gca().transAxes, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            
            plt.tight_layout()
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            raise Exception(f"Ошибка при создании графика длительности: {e}")