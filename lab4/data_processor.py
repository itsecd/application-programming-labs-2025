import os
import cv2
import pandas as pd
from typing import Tuple, List, Optional


class DataFrameProcessor:
    """
    Класс для работы с DataFrame: загрузка, обработка изображений,
    вычисление статистики, сортировка и фильтрация.
    """

    def __init__(self, csv_path: str) -> None:
        """
        Инициализация процессора и загрузка данных.

        :param csv_path: Абсолютный или относительный путь к CSV-файлу.
        :raises FileNotFoundError: Если файл не найден.
        """
        self.csv_full_path = os.path.abspath(csv_path)
        self.csv_dir = os.path.dirname(self.csv_full_path)

        if not os.path.exists(self.csv_full_path):
            raise FileNotFoundError(f"Файл аннотации не найден: {self.csv_full_path}")

        try:
            self.df: pd.DataFrame = pd.read_csv(self.csv_full_path)
        except Exception as e:
            raise IOError(f"Ошибка при чтении CSV файла: {e}")

    def rename_columns(self) -> None:
        """
        ереименование колонок: 'Абсолютный путь' и 'Относительный путь'.
        """
        new_names = {
            "Абсолютный путь": "absolute_path",
            "Относительный путь": "relative_path"
        }
        if all(col in self.df.columns for col in new_names.keys()):
            self.df.rename(columns=new_names, inplace=True)

    def _resolve_path(self, row: pd.Series) -> Optional[str]:
        """
        Умный поиск реального пути к изображению, учитывая перемещение папок.

        :param row: Строка DataFrame.
        :return: Корректный путь к файлу или None.
        """
        abs_p = row.get('absolute_path')
        if abs_p and os.path.exists(abs_p):
            return abs_p

        rel_p = row.get('relative_path')
        if rel_p:
            clean_rel = rel_p.replace('\\', '/').lstrip('./')
            candidate = os.path.join(self.csv_dir, clean_rel)
            if os.path.exists(candidate):
                return candidate

        return None

    def add_brightness_ranges(self) -> None:
        """
        Добавление колонок с диапазонами яркости (max-min) по каналам R, G, B.
        """
        r_vals, g_vals, b_vals = [], [], []

        for idx, row in self.df.iterrows():
            real_path = self._resolve_path(row)

            if not real_path:
                stats = (-1, -1, -1)
            else:
                stats = self._calculate_image_stats(real_path)

            r_range, g_range, b_range = stats

            r_vals.append(r_range)
            g_vals.append(g_range)
            b_vals.append(b_range)

        self.df["r_range"] = r_vals
        self.df["g_range"] = g_vals
        self.df["b_range"] = b_vals

        self.df["r_bin"] = self.df["r_range"].apply(self._get_bin_label)
        self.df["g_bin"] = self.df["g_range"].apply(self._get_bin_label)
        self.df["b_bin"] = self.df["b_range"].apply(self._get_bin_label)
        print("Колонки диапазонов яркости добавлены.")

    def sort_by_column(self, column: str, ascending: bool = True) -> pd.DataFrame:
        """
        Реализация функции сортировки.

        :param column: Имя колонки (например, 'r_range').
        :param ascending: Сортировка по возрастанию (True) или убыванию (False).
        :return: Отсортированный DataFrame.
        :raises KeyError: Если колонка не найдена.
        """
        if column not in self.df.columns:
            raise KeyError(f"Колонка {column} отсутствует для сортировки.")
        return self.df.sort_values(by=column, ascending=ascending, inplace=False)

    def filter_by_value(self, column: str, value: str) -> pd.DataFrame:
        """
        Реализация функции фильтрации по точному значению.

        :param column: Имя колонки (например, 'r_bin').
        :param value: Значение для фильтрации (например, '101-150').
        :return: Новый отфильтрованный DataFrame.
        :raises KeyError: Если колонка не найдена.
        """
        if column not in self.df.columns:
            raise KeyError(f"Колонка {column} отсутствует для фильтрации.")
        return self.df[self.df[column] == value].copy()

    def save_csv(self, output_path: str) -> None:
        """
        7) Сохраняет текущий DataFrame в CSV.

        :param output_path: Путь сохранения.
        """
        self.df.to_csv(output_path, index=False, encoding='utf-8-sig')

    @staticmethod
    def _calculate_image_stats(image_path: str) -> Tuple[int, int, int]:
        """
        Вычисляет диапазон яркости (max - min) для каналов R, G, B.
        """
        img = cv2.imread(image_path)
        if img is None:
            return -1, -1, -1  # Код ошибки

        b_ch, g_ch, r_ch = cv2.split(img)

        r_diff = int(r_ch.max()) - int(r_ch.min())
        g_diff = int(g_ch.max()) - int(g_ch.min())
        b_diff = int(b_ch.max()) - int(b_ch.min())

        return r_diff, g_diff, b_diff

    @staticmethod
    def _get_bin_label(value: int) -> str:
        """Определяет категорию диапазона для гистограммы."""
        if value < 0: return "Error"
        if value <= 50:
            return "0-50"
        elif value <= 100:
            return "51-100"
        elif value <= 150:
            return "101-150"
        elif value <= 200:
            return "151-200"
        else:
            return "201-255"