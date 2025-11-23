from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Visualizer:
    """Класс для визуализации данных."""

    def __init__(self, brightness_ranges: List[Tuple[int, int, str]]):
        self.brightness_ranges = brightness_ranges
        self.range_names = [r[2] for r in brightness_ranges]

    def plot_channel_histograms(self, df: pd.DataFrame, output_file: str):
        """Строит гистограммы распределения яркости по каналам RGB."""
        try:
            # Фильтруем только строки с данными о яркости
            valid_df = df[df['brightness_range'] != '']
            if len(valid_df) == 0:
                return

            # Суммируем гистограммы для всех изображений
            total_r_hist = np.sum([hist for hist in valid_df['r_histogram']], axis=0)
            total_g_hist = np.sum([hist for hist in valid_df['g_histogram']], axis=0)
            total_b_hist = np.sum([hist for hist in valid_df['b_histogram']], axis=0)

            x = np.arange(len(self.range_names))
            width = 0.25

            fig, ax = plt.subplots(figsize=(12, 8))

            bars1 = ax.bar(x - width, total_r_hist, width, label='Red Channel',
                          color='red', alpha=0.7, edgecolor='black')
            bars2 = ax.bar(x, total_g_hist, width, label='Green Channel',
                          color='green', alpha=0.7, edgecolor='black')
            bars3 = ax.bar(x + width, total_b_hist, width, label='Blue Channel',
                          color='blue', alpha=0.7, edgecolor='black')

            # Добавляем значения на столбцы
            self._add_value_labels(ax, bars1)
            self._add_value_labels(ax, bars2)
            self._add_value_labels(ax, bars3)

            ax.set_xlabel('Диапазоны яркости', fontsize=12)
            ax.set_ylabel('Количество файлов', fontsize=12)
            ax.set_title('Распределение яркости по каналам RGB', fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(self.range_names, fontsize=11)
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3, axis='y')

            plt.tight_layout()
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            plt.close()

        except Exception as e:
            raise Exception(f"Ошибка построения гистограмм каналов: {e}")

    def plot_brightness_distribution(self, df: pd.DataFrame, output_file: str):
        """Строит гистограмму распределения файлов по диапазонам яркости."""
        try:
            # Фильтруем только строки с данными о яркости
            valid_df = df[df['brightness_range'] != '']
            if len(valid_df) == 0:
                return

            brightness_counts = valid_df['brightness_range'].value_counts()
            brightness_counts = brightness_counts.reindex(self.range_names, fill_value=0)

            plt.figure(figsize=(10, 6))
            bars = plt.bar(brightness_counts.index, brightness_counts.values,
                          color=['#ff6b6b', '#51cf66', '#339af0'][:len(self.range_names)],
                          alpha=0.7, edgecolor='black')

            # Добавляем значения на столбцы
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom', fontweight='bold')

            plt.xlabel('Диапазоны яркости', fontsize=12)
            plt.ylabel('Количество файлов', fontsize=12)
            plt.title('Распределение файлов по диапазонам яркости', fontsize=14, fontweight='bold')
            plt.xticks(fontsize=11)
            plt.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()

            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            plt.close()

        except Exception as e:
            raise Exception(f"Ошибка построения распределения яркости: {e}")

    def _add_value_labels(self, ax, bars):
        """Добавляет числовые значения на столбцы гистограммы."""
        for bar in bars:
            height = bar.get_height()
            if height > 0: 
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom',
                       fontweight='bold', fontsize=10)