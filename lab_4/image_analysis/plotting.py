import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Tuple
import numpy as np


def create_width_distribution_plot(
    df: pd.DataFrame, 
    output_path: str,
    figsize: Tuple[int, int] = (14, 6)
) -> None:
    """
    Создает график распределения ширины изображений.
    """
    if df.empty:
        raise ValueError("DataFrame пустой")
    
    if 'image_width' not in df.columns:
        raise ValueError("DataFrame не содержит колонку 'image_width'")
    
    output_dir = Path(output_path).parent
    if output_dir != Path('.'):
        output_dir.mkdir(parents=True, exist_ok=True)
    
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    
    # График: Ширина изображений по порядку
    _plot_width_sequence(ax, df)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()


def _plot_width_sequence(ax: plt.Axes, df: pd.DataFrame) -> None:
    """
    Создает линейный график ширины изображений по порядку.
    """
    widths = df['image_width'].values
    indices = np.arange(len(df))
    
    ax.plot(indices, widths, linewidth=1.5, color='steelblue', 
            marker='o', markersize=3, alpha=0.7)
    
    ax.set_xlabel('Номер изображения в отсортированном списке', fontsize=12)
    ax.set_ylabel('Ширина изображения (пиксели)', fontsize=12)
    ax.set_title('Распределение ширины изображений (отсортировано по возрастанию)', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(-1, len(df))