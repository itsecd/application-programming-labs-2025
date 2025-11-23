import matplotlib.pyplot as plt
import pandas as pd
from typing import List


class HistogramPlotter:
    """
    Класс для визуализации данных. Не зависит от логики обработки данных.
    """

    def __init__(self, df: pd.DataFrame, bin_order: List[str]) -> None:
        """
        :param df: Данные.
        :param bin_order: Список меток категорий (ось X) в нужном порядке.
        """
        self.df = df
        self.bin_order = bin_order

    def plot_rgb_histograms(self, output_path: str, sorted_data: pd.DataFrame) -> None:
        fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

        channels = [
            ('r_bin', 'Red Channel Range', 'red'),
            ('g_bin', 'Green Channel Range', 'green'),
            ('b_bin', 'Blue Channel Range', 'blue')
        ]

        try:
            for ax, (col_name, title, color) in zip(axes, channels):
                counts = sorted_data[col_name].value_counts().reindex(
                    self.bin_order, fill_value=0
                )

                ax.bar(counts.index, counts.values, color=color, alpha=0.7, edgecolor='black')

                ax.set_title(title, fontsize=12)
                ax.set_xlabel('Range (Max-Min)', fontsize=10)
                ax.set_ylabel('Count', fontsize=10)
                ax.tick_params(axis='x', rotation=45)
                ax.grid(axis='y', linestyle='--', alpha=0.5)

            plt.tight_layout()
            plt.savefig(output_path)
            print(f"График сохранен: {output_path}")

        except Exception as e:
            print(f"Ошибка при построении графика: {e}")
        finally:
            plt.close(fig)