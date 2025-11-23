"""Модуль для визуализации данных."""
import matplotlib.pyplot as plt


class DataVisualizer:
    """Класс для визуализации данных."""

    def __init__(self):
        """Инициализация визуализатора."""
        pass

    def plot_brightness_distribution(self, sorted_df, output_plot):
        """
        Строит график яркости отсортированных изображений.

        Args:
            sorted_df: Отсортированный DataFrame
            output_plot: Имя файла для сохранения графика
        """
        plt.figure(figsize=(12, 6))

        plt.plot(
            range(len(sorted_df)),
            sorted_df['Средняя_яркость'],
            marker='o',
            linestyle='-',
            linewidth=1,
            markersize=3,
            alpha=0.7
        )

        plt.title(
            'Распределение средней яркости изображений птиц',
            fontsize=14,
            pad=20
        )
        plt.xlabel('Номер изображения в отсортированном списке', fontsize=12)
        plt.ylabel('Средняя яркость', fontsize=12)

        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        plt.savefig(output_plot, dpi=300, bbox_inches='tight')
        plt.close()