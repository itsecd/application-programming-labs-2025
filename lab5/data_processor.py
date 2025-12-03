import cv2
import os
import pandas as pd
import numpy as np
from typing import Tuple, List, Optional


class DataFrameProcessor:
    """
    Класс для работы с DataFrame: загрузка, обработка изображений,
    вычисление статистики, сортировка и фильтрация.
    """

    def __init__(self, csv_path: str) -> None:
        self.csv_full_path = os.path.abspath(csv_path)
        self.csv_dir = os.path.dirname(self.csv_full_path)

        if not os.path.exists(self.csv_full_path):
            raise FileNotFoundError(f"Файл аннотации не найден: {self.csv_full_path}")

        try:
            self.df: pd.DataFrame = pd.read_csv(self.csv_full_path)
        except Exception as e:
            raise IOError(f"Ошибка при чтении CSV файла: {e}")

        self.current_bin_order: List[str] = []

    def rename_columns(self) -> None:
        new_names = {
            "Абсолютный путь": "absolute_path",
            "Относительный путь": "relative_path"
        }
        if all(col in self.df.columns for col in new_names.keys()):
            self.df.rename(columns=new_names, inplace=True)

    def _resolve_path(self, row: pd.Series) -> Optional[str]:
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

    def add_brightness_ranges(self, user_bins: List[int]) -> None:
        """
        Добавляет колонки с диапазонами яркости на основе пользовательских границ.
        Использует pd.cut для эффективного разбиения.
        """
        r_vals, g_vals, b_vals = [], [], []

        for _, row in self.df.iterrows():
            real_path = self._resolve_path(row)
            if not real_path:
                stats = (-1, -1, -1)
            else:
                stats = self._calculate_image_stats(real_path)

            r_vals.append(stats[0])
            g_vals.append(stats[1])
            b_vals.append(stats[2])

        self.df["r_range"] = r_vals
        self.df["g_range"] = g_vals
        self.df["b_range"] = b_vals


        bins_edges = [-1] + user_bins
        if bins_edges[-1] < 255:
            bins_edges.append(255)
        labels = []
        start = 0
        for edge in user_bins:
            labels.append(f"{start}-{edge}")
            start = edge + 1

        if start <= 255:
            labels.append(f"{start}-255")

        self.current_bin_order = labels + ["Error"]

        def get_label(val: int) -> str:
            if val < 0: return "Error"
            if val > 255: return f"256+"

            s = 0
            for edge, label in zip(user_bins, labels):
                if val <= edge:
                    return label
                s = edge
            return labels[-1]

        self.df["r_bin"] = self.df["r_range"].apply(get_label)
        self.df["g_bin"] = self.df["g_range"].apply(get_label)
        self.df["b_bin"] = self.df["b_range"].apply(get_label)

    def get_bin_order(self) -> List[str]:
        """Возвращает список меток в правильном порядке для графика."""
        return self.current_bin_order

    def sort_by_column(self, column: str, ascending: bool = True) -> pd.DataFrame:
        if column not in self.df.columns:
            raise KeyError(f"Колонка {column} отсутствует.")
        return self.df.sort_values(by=column, ascending=ascending, inplace=False)

    def filter_by_value(self, column: str, value: str) -> pd.DataFrame:
        if column not in self.df.columns:
            raise KeyError(f"Колонка {column} отсутствует.")
        return self.df[self.df[column] == value].copy()

    def save_csv(self, output_path: str) -> None:
        self.df.to_csv(output_path, index=False, encoding='utf-8-sig')

    @staticmethod
    def _calculate_image_stats(image_path: str) -> Tuple[int, int, int]:
        img = cv2.imread(image_path)
        if img is None:
            return -1, -1, -1
        b, g, r = cv2.split(img)
        return (int(r.max()) - int(r.min()),
                int(g.max()) - int(g.min()),
                int(b.max()) - int(b.min()))