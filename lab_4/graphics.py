"""Модуль для визуализации и сохранения результатов."""
import matplotlib.pyplot as plt
import pandas as pd
from typing import Union


def create_graph(df: pd.DataFrame) -> Union[plt.Figure, None]:
    """Создание гистограммы распределения яркости по диапазонам."""
    if df.empty or 'Brightness_range_label' not in df.columns:
        return None
    
    def get_min_from_label(label: str) -> int:
        """Получение минимального значения из метки диапазона."""
        try:
            if '-' in label:
                return int(label.split('-')[0])
            else:
                return int(label)
        except (ValueError, AttributeError):
            return 0
    
    range_labels = sorted(
        df['Brightness_range_label'].unique(), 
        key=get_min_from_label
    )
    
    range_counts = df['Brightness_range_label'].value_counts()
    range_counts = range_counts.reindex(range_labels).fillna(0)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.bar(
        range_labels, 
        range_counts.values, 
        alpha=0.7, 
        color='skyblue', 
        edgecolor='black'
    )
    
    for bar, count in zip(bars, range_counts.values):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0, 
            height + 0.5,
            f'{int(count)}', 
            ha='center', 
            va='bottom', 
            fontsize=10
        )
    
    ax.set_title('Гистограмма распределения изображений по диапазонам яркости')
    ax.set_xlabel('Диапазон яркости')
    ax.set_ylabel('Количество изображений')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.xticks(rotation=45, ha='right')
    
    total_images = len(df)
    ax.text(
        0.02, 
        0.98, 
        f'Всего изображений: {total_images}',
        transform=ax.transAxes, 
        fontsize=12,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    )
    
    plt.tight_layout()
    return fig


def save_dataframe_to_csv(
    df: pd.DataFrame, 
    filename: str = 'brightness_analysis.csv'
) -> None:
    """Сохранение DataFrame в CSV файл."""
    df.to_csv(filename, index=False, encoding='utf-8')


def save_plot_to_file(fig: plt.Figure, filename: str) -> None:
    """Сохранение графика в файл."""
    if fig is not None:
        fig.savefig(filename, dpi=300, bbox_inches='tight')