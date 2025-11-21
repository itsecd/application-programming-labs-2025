import os
from typing import Dict, List, Tuple

import pandas as pd

class DataFrameManager:
    """Класс для работы с DataFrame изображений."""

    def __init__(self):
        self.df = None

    def create_from_annotation(self, annotation_file: str) -> pd.DataFrame:
        """Создает DataFrame из CSV аннотации."""
        try:
            self.df = pd.read_csv(annotation_file)
            # Переименовываем колонки 
            self.df.columns = ['absolute_path', 'relative_path']
            print(f"Успешно загружено {len(self.df)} записей из аннотации")
            return self.df
        except Exception as e:
            raise Exception(f"Ошибка создания DataFrame: {e}")

    def get_valid_image_paths(self) -> List[str]:
        """Возвращает список существующих путей к изображениям."""
        valid_paths = []

        for idx, row in self.df.iterrows():
            # Пробуем сначала относительный путь, потом абсолютный
            rel_path = row['relative_path']
            abs_path = row['absolute_path']

            if os.path.exists(rel_path):
                valid_paths.append(rel_path)
            elif os.path.exists(abs_path):
                valid_paths.append(abs_path)
            else:
                print(f"  Файл не найден: {rel_path}")

        print(f"  Найдено {len(valid_paths)} существующих файлов из {len(self.df)}")
        return valid_paths

    def add_brightness_columns(self, image_paths: List[str], brightness_data: List[dict]):
        """Добавляет колонки с данными о яркости."""
        try:
            # Создаем маппинг путь -> данные
            path_to_data = {data['image_path']: data for data in brightness_data}

            self.df['brightness_range'] = ''
            self.df['r_histogram'] = None
            self.df['g_histogram'] = None
            self.df['b_histogram'] = None
            self.df['r_channel_range'] = ''
            self.df['g_channel_range'] = ''
            self.df['b_channel_range'] = ''

            processed_count = 0
            for idx, row in self.df.iterrows():
                rel_path = row['relative_path']
                abs_path = row['absolute_path']

                for path in [rel_path, abs_path]:
                    if path in path_to_data:
                        data = path_to_data[path]
                        self.df.at[idx, 'brightness_range'] = data['brightness_range']
                        self.df.at[idx, 'r_histogram'] = data['r_histogram']
                        self.df.at[idx, 'g_histogram'] = data['g_histogram']
                        self.df.at[idx, 'b_histogram'] = data['b_histogram']
                        self.df.at[idx, 'r_channel_range'] = data['r_channel']
                        self.df.at[idx, 'g_channel_range'] = data['g_channel']
                        self.df.at[idx, 'b_channel_range'] = data['b_channel']
                        processed_count += 1
                        break

            print(f"Данные о яркости добавлены для {processed_count} изображений")

        except Exception as e:
            raise Exception(f"Ошибка добавления колонок яркости: {e}")

    def sort_by_brightness(self) -> pd.DataFrame:
        """Сортирует DataFrame по диапазону яркости."""
        try:
            # Создаем порядок сортировки для диапазонов
            range_order = {"0-85": 0, "86-170": 1, "171-255": 2}
            df_sorted = self.df.copy()
            df_sorted['sort_order'] = df_sorted['brightness_range'].map(range_order)
            df_sorted = df_sorted.sort_values('sort_order').drop('sort_order', axis=1)

            print("DataFrame отсортирован по яркости")
            return df_sorted

        except Exception as e:
            raise Exception(f"Ошибка сортировки: {e}")

    def filter_by_brightness(self, brightness_range: str) -> pd.DataFrame:
        """Фильтрует DataFrame по диапазону яркости."""
        try:
            filtered_df = self.df[self.df['brightness_range'] == brightness_range]
            print(f"Отфильтровано {len(filtered_df)} с диапазоном '{brightness_range}'")
            return filtered_df
        except Exception as e:
            raise Exception(f"Ошибка фильтрации: {e}")

    def save_to_csv(self, output_file: str):
        """Сохраняет DataFrame в CSV файл."""
        try:
            # Сохраняем только основные колонки для читаемости
            columns_to_save = [
                'absolute_path', 'relative_path', 'brightness_range',
                'r_channel_range', 'g_channel_range', 'b_channel_range'
            ]
            self.df[columns_to_save].to_csv(output_file, index=False)
            print(f"DataFrame сохранен в {output_file}")
        except Exception as e:
            raise Exception(f"Ошибка сохранения DataFrame: {e}")

    def print_brightness_stats(self):
        """Выводит статистику по диапазонам яркости."""
        if self.df is not None and 'brightness_range' in self.df.columns:
            # Фильтруем только строки с данными о яркости
            valid_data = self.df[self.df['brightness_range'] != '']
            if len(valid_data) > 0:
                stats = valid_data['brightness_range'].value_counts()
                print("\nСтатистика по диапазонам яркости:")
                for range_name, count in stats.items():
                    print(f"  {range_name}: {count} файлов")
            else:
                print("\nНет данных о яркости для отображения статистики")