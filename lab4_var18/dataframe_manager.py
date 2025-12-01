"""Модуль для работы с DataFrame и анализа данных."""
import os
from typing import Any, Dict, List

import pandas as pd

from audio_processor import AudioProcessor


class DataFrameManager:
    """Класс для управления DataFrame с аудиофайлами."""

    def __init__(self):
        """Инициализирует менеджер DataFrame."""
        self.df = pd.DataFrame()
        self.audio_processor = AudioProcessor()

    def create_dataframe_from_annotation(self, csv_path: str) -> pd.DataFrame:
        """
        Создает DataFrame из CSV аннотации.

        Args:
            csv_path: Путь к CSV файлу аннотации

        Returns:
            DataFrame с путями к файлам

        Raises:
            FileNotFoundError: Если файл аннотации не найден
            Exception: Если произошла ошибка при создании DataFrame
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Файл аннотации не найден: {csv_path}")

        try:
            self.df = pd.read_csv(csv_path)
            
            column_mapping = {
                'name': 'audio_name',
                'absolute_path': 'absolute_file_path', 
                'relative_path': 'relative_file_path'
            }
            
            existing_columns = {k: v for k, v in column_mapping.items() 
                              if k in self.df.columns}
            self.df = self.df.rename(columns=existing_columns)
            
            return self.df
            
        except Exception as e:
            raise Exception(f"Ошибка при создании DataFrame: {e}")

    def add_duration_column(self) -> None:
        """
        Добавляет колонку с длительностью аудиофайлов.

        Raises:
            ValueError: Если отсутствует колонка с абсолютными путями
            Exception: Если произошла ошибка при добавлении колонки
        """
        if 'absolute_file_path' not in self.df.columns:
            raise ValueError("Отсутствует колонка с абсолютными путями")

        try:
            self.df['duration_seconds'] = self.df['absolute_file_path'].apply(
                lambda x: self.audio_processor.get_audio_duration(x) 
                if pd.notna(x) and os.path.exists(x) else 0.0
            )
        except Exception as e:
            raise Exception(f"Ошибка при добавлении колонки с длительностью: {e}")

    def sort_by_duration(self, ascending: bool = True) -> pd.DataFrame:
        """
        Сортирует DataFrame по длительности.

        Args:
            ascending: Порядок сортировки (по возрастанию/убыванию)

        Returns:
            Отсортированный DataFrame

        Raises:
            Exception: Если произошла ошибка при сортировке
        """
        try:
            if 'duration_seconds' not in self.df.columns:
                self.add_duration_column()

            sorted_df = self.df.sort_values('duration_seconds', ascending=ascending)
            return sorted_df
            
        except Exception as e:
            raise Exception(f"Ошибка при сортировке: {e}")

    def filter_by_duration(self, min_duration: float = 0, max_duration: float = None) -> pd.DataFrame:
        """
        Фильтрует DataFrame по длительности.

        Args:
            min_duration: Минимальная длительность в секундах
            max_duration: Максимальная длительность в секундах

        Returns:
            Отфильтрованный DataFrame

        Raises:
            Exception: Если произошла ошибка при фильтрации
        """
        try:
            if 'duration_seconds' not in self.df.columns:
                self.add_duration_column()

            filtered_df = self.df[self.df['duration_seconds'] >= min_duration]
            
            if max_duration is not None:
                filtered_df = filtered_df[filtered_df['duration_seconds'] <= max_duration]

            return filtered_df
            
        except Exception as e:
            raise Exception(f"Ошибка при фильтрации: {e}")

    def save_dataframe(self, output_path: str) -> None:
        """
        Сохраняет DataFrame в CSV файл.

        Args:
            output_path: Путь для сохранения

        Raises:
            Exception: Если произошла ошибка при сохранении
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            result_df = self.df[['absolute_file_path', 'relative_file_path', 'duration_seconds']]
            
            result_df.to_csv(
                output_path, 
                index=False, 
                encoding='utf-8-sig',
                sep=','
            )
            
        except Exception as e:
            raise Exception(f"Ошибка при сохранении DataFrame: {e}")

    def get_dataframe_info(self) -> Dict[str, Any]:
        """
        Возвращает информацию о DataFrame.

        Returns:
            Словарь с информацией о DataFrame
        """
        info = {
            'total_files': len(self.df),
            'columns': list(self.df.columns)
        }
        
        if 'duration_seconds' in self.df.columns:
            info.update({
                'total_duration': round(self.df['duration_seconds'].sum(), 2),
                'average_duration': round(self.df['duration_seconds'].mean(), 2),
                'max_duration': round(self.df['duration_seconds'].max(), 2),
                'min_duration': round(self.df['duration_seconds'].min(), 2)
            })
        
        return info