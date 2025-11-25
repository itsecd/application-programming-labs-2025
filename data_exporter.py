"""
Модуль для экспорта данных об амплитудах.
"""

import pandas as pd
from typing import Optional


class DataExporter:
    """Класс для экспорта данных об амплитудах."""
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame, filename: str = 'audio_data_with_amplitude.csv') -> None:
        """
        Экспортирует DataFrame в CSV файл.
        
        Args:
            df: DataFrame для экспорта
            filename: Имя файла для сохранения
        """
        output_df = df[['Абсолютный_путь_к_файлу', 'Относительный_путь_к_файлу', 
                       'Максимальная_амплитуда']]
        output_df.to_csv(filename, index=False, encoding='utf-8')
        print(f"DataFrame сохранен как '{filename}'")
    
    @staticmethod
    def print_statistics(stats: dict, top_files: pd.DataFrame) -> None:
        """
        Выводит статистику и топ файлов в консоль.
        
        Args:
            stats: Словарь со статистикой
            top_files: DataFrame с топ файлами
        """
        print("\n" + "="*50)
        print("СТАТИСТИКА ПО АМПЛИТУДАМ:")
        print(f"Всего файлов: {stats['total_files']}")
        print(f"Максимальная амплитуда: {stats['max_amplitude']:.4f}")
        print(f"Минимальная амплитуда: {stats['min_amplitude']:.4f}")
        print(f"Средняя амплитуда: {stats['mean_amplitude']:.4f}")
        print(f"Медианная амплитуда: {stats['median_amplitude']:.4f}")
        
        print("\nТОП-5 файлов с наибольшей амплитудой:")
        for idx, row in top_files.iterrows():
            print(f"  {row['Имя_файла']}: {row['Максимальная_амплитуда']:.4f}")