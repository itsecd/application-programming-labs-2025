from __future__ import annotations
import matplotlib.pyplot as plt
import pandas as pd

def plot_aspect_ratios(
    df_sorted: pd.DataFrame,
    save_path: str = "aspect_ratio_plot.png"
) -> None:
    """Строит и сохраняет график отношения сторон.

    Args:
        df_sorted (pd.DataFrame): Отсортированный по aspect_ratio DataFrame.
        save_path (str): Путь для сохранения графика.
    """
    ratios = df_sorted['aspect_ratio']
    x_labels = list(range(1, len(ratios) + 1))

    plt.figure(figsize=(14, 7))
    plt.plot(x_labels, ratios, 'o-', color='#2E86AB', markersize=6, linewidth=2,
             label='Отношение сторон (ширина / высота)')
    plt.fill_between(x_labels, ratios, alpha=0.1, color='#2E86AB')

    plt.title('Отношение сторон изображений\n(отсортировано по убыванию)', 
              fontsize=16, pad=20)
    plt.xlabel('Номер изображения в отсортированном списке', fontsize=12)
    plt.ylabel('Отношение сторон (ширина / высота)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()