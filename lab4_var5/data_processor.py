"""Модуль для обработки данных и работы с DataFrame."""
import pandas as pd


class DataProcessor:
    """Класс для обработки данных и работы с DataFrame."""

    def __init__(self):
        """Инициализация процессора данных."""
        self.df = None

    def load_annotation_data(self, annotation_file):
        """
        Загружает данные из аннотации и создает DataFrame.

        Args:
            annotation_file: Путь к файлу аннотации CSV

        Returns:
            pandas.DataFrame: Загруженный DataFrame
        """
        self.df = pd.read_csv(annotation_file)

        self.df = self.df.rename(columns={
            'absolute_path': 'Абсолютный_путь',
            'relative_path': 'Относительный_путь'
        })

        self.df = self.df[['Абсолютный_путь', 'Относительный_путь']]

        return self.df

    def add_brightness_column(self, brightness_values):
        """
        Добавляет колонку со значениями яркости.

        Args:
            brightness_values: Список значений яркости

        Returns:
            pandas.DataFrame: DataFrame с добавленной колонкой
        """
        if self.df is None:
            raise ValueError("DataFrame не загружен. Сначала вызовите load_annotation_data")

        self.df['Средняя_яркость'] = brightness_values
        return self.df

    def sort_by_brightness(self, ascending=True):
        """
        Сортирует DataFrame по колонке с яркостью.

        Args:
            ascending: Порядок сортировки

        Returns:
            pandas.DataFrame: Отсортированный DataFrame
        """
        if self.df is None or 'Средняя_яркость' not in self.df.columns:
            raise ValueError("DataFrame не содержит колонку с яркостью")

        sorted_df = self.df.sort_values('Средняя_яркость', ascending=ascending)
        return sorted_df.reset_index(drop=True)

    def filter_by_brightness(self, min_brightness=None, max_brightness=None):
        """
        Фильтрует DataFrame по диапазону яркости.

        Args:
            min_brightness: Минимальная яркость
            max_brightness: Максимальная яркость

        Returns:
            pandas.DataFrame: Отфильтрованный DataFrame
        """
        if self.df is None or 'Средняя_яркость' not in self.df.columns:
            raise ValueError("DataFrame не содержит колонку с яркостью")

        filtered_df = self.df.copy()

        if min_brightness is not None:
            filtered_df = filtered_df[filtered_df['Средняя_яркость'] >= min_brightness]

        if max_brightness is not None:
            filtered_df = filtered_df[filtered_df['Средняя_яркость'] <= max_brightness]

        return filtered_df.reset_index(drop=True)

    def get_statistics(self):
        """
        Возвращает статистику по данным.

        Returns:
            dict: Словарь со статистикой
        """
        if self.df is None or 'Средняя_яркость' not in self.df.columns:
            raise ValueError("DataFrame не содержит колонку с яркостью")

        return {
            'total_images': len(self.df),
            'min_brightness': round(self.df['Средняя_яркость'].min(), 2),
            'max_brightness': round(self.df['Средняя_яркость'].max(), 2),
            'mean_brightness': round(self.df['Средняя_яркость'].mean(), 2),
            'median_brightness': round(self.df['Средняя_яркость'].median(), 2)
        }

    def save_dataframe(self, output_file):
        """
        Сохраняет DataFrame в CSV файл.

        Args:
            output_file: Путь для сохранения файла
        """
        if self.df is None:
            raise ValueError("Нет данных для сохранения")

        self.df.to_csv(output_file, index=False, encoding='utf-8')