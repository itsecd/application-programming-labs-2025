"""
Модуль для анализа аудиофайлов и работы с данными об амплитудах.
"""

import os
from pathlib import Path
from typing import Tuple, Optional, List, Dict, Any

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import librosa


class AudioAnalyzer:
    """Класс для анализа аудиофайлов и работы с данными об амплитудах."""
    
    def __init__(self, csv_path: str) -> None:
        """
        Инициализация анализатора аудиофайлов.
        
        Args:
            csv_path: Путь к CSV файлу с метаданными аудиофайлов
        """
        self.csv_path = csv_path
        self.df: Optional[pd.DataFrame] = None
        self.df_sorted: Optional[pd.DataFrame] = None
        self.df_filtered: Optional[pd.DataFrame] = None
        
    def load_data(self) -> None:
        """
        Загрузка данных из CSV файла и переименование колонок.
        
        Raises:
            FileNotFoundError: Если CSV файл не найден
            pd.errors.EmptyDataError: Если CSV файл пустой
            pd.errors.ParserError: Если ошибка парсинга CSV
        """
        try:
            self.df = pd.read_csv(self.csv_path)
            
            # Переименование колонок для отражения содержимого
            column_mapping = {
                'absolute_path': 'Абсолютный_путь_к_файлу',
                'relative_path': 'Относительный_путь_к_файлу',
                'filename': 'Имя_файла',
                'duration_seconds': 'Длительность_секунды',
                'file_size_mb': 'Размер_файла_МБ'
            }
            
            self.df = self.df.rename(columns=column_mapping)
            print(f"Данные успешно загружены. Записей: {len(self.df)}")
            
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV файл не найден: {self.csv_path}")
        except pd.errors.EmptyDataError:
            raise pd.errors.EmptyDataError("CSV файл пустой")
        except pd.errors.ParserError as e:
            raise pd.errors.ParserError(f"Ошибка парсинга CSV: {e}")
    
    def get_max_amplitude(self, file_path: str) -> float:
        """
        Получает максимальную амплитуду аудиофайла по модулю.
        
        Args:
            file_path: Путь к аудиофайлу
            
        Returns:
            Максимальная амплитуда аудиофайла
        """
        try:
            # Проверяем существование файла
            if not os.path.exists(file_path):
                print(f"Файл не найден: {file_path}")
                return 0.0
            
            # Загружаем аудиофайл с помощью librosa
            audio_data, sample_rate = librosa.load(file_path, sr=None)
            
            # Находим максимальную амплитуду по модулю
            max_amplitude = np.max(np.abs(audio_data))
            
            return max_amplitude
            
        except Exception as e:
            print(f"Ошибка при обработке файла {file_path}: {e}")
            return 0.0
    
    def add_amplitude_column(self) -> None:
        """
        Добавляет колонку с максимальной амплитудой в DataFrame.
        
        Raises:
            ValueError: Если данные не загружены
        """
        if self.df is None:
            raise ValueError("Данные не загружены. Сначала вызовите load_data()")
        
        print("Добавление колонки с максимальной амплитудой...")
        self.df['Максимальная_амплитуда'] = self.df['Абсолютный_путь_к_файлу'].apply(
            self.get_max_amplitude
        )
    
    def sort_by_amplitude(self, ascending: bool = True) -> pd.DataFrame:
        """
        Сортирует DataFrame по колонке максимальной амплитуды.
        
        Args:
            ascending: Порядок сортировки (True - по возрастанию, False - по убыванию)
            
        Returns:
            Отсортированный DataFrame
            
        Raises:
            ValueError: Если данные не загружены или колонка амплитуды не добавлена
        """
        if self.df is None or 'Максимальная_амплитуда' not in self.df.columns:
            raise ValueError("Данные не загружены или колонка амплитуды не добавлена")
        
        self.df_sorted = self.df.sort_values('Максимальная_амплитуда', ascending=ascending)
        order = "возрастанию" if ascending else "убыванию"
        print(f"Данные отсортированы по {order} максимальной амплитуды")
        
        return self.df_sorted
    
    def filter_by_amplitude(self, min_amplitude: float = 0.0, 
                           max_amplitude: float = 1.0) -> pd.DataFrame:
        """
        Фильтрует DataFrame по диапазону максимальной амплитуды.
        
        Args:
            min_amplitude: Минимальная амплитуда
            max_amplitude: Максимальная амплитуда
            
        Returns:
            Отфильтрованный DataFrame
            
        Raises:
            ValueError: Если данные не загружены или колонка амплитуды не добавлена
        """
        if self.df is None or 'Максимальная_амплитуда' not in self.df.columns:
            raise ValueError("Данные не загружены или колонка амплитуды не добавлена")
        
        self.df_filtered = self.df[
            (self.df['Максимальная_амплитуда'] >= min_amplitude) & 
            (self.df['Максимальная_амплитуда'] <= max_amplitude)
        ]
        
        print(f"После фильтрации осталось {len(self.df_filtered)} файлов из {len(self.df)}")
        
        return self.df_filtered
    
    def get_amplitude_statistics(self) -> Dict[str, Any]:
        """
        Возвращает статистику по амплитудам.
        
        Returns:
            Словарь со статистикой
            
        Raises:
            ValueError: Если данные не загружены или колонка амплитуды не добавлена
        """
        if self.df is None or 'Максимальная_амплитуда' not in self.df.columns:
            raise ValueError("Данные не загружены или колонка амплитуды не добавлена")
        
        stats = {
            'total_files': len(self.df),
            'max_amplitude': self.df['Максимальная_амплитуда'].max(),
            'min_amplitude': self.df['Максимальная_амплитуда'].min(),
            'mean_amplitude': self.df['Максимальная_амплитуда'].mean(),
            'median_amplitude': self.df['Максимальная_амплитуда'].median()
        }
        
        return stats
    
    def get_top_files(self, n: int = 5) -> pd.DataFrame:
        """
        Возвращает топ-N файлов с наибольшей амплитудой.
        
        Args:
            n: Количество файлов для возврата
            
        Returns:
            DataFrame с топ-N файлами
            
        Raises:
            ValueError: Если данные не отсортированы
        """
        if self.df_sorted is None:
            raise ValueError("Данные не отсортированы. Сначала вызовите sort_by_amplitude()")
        
        return self.df_sorted.head(n)[['Имя_файла', 'Максимальная_амплитуда']]