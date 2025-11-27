"""Модуль для визуализации и сохранения результатов."""
import matplotlib.pyplot as plt
import pandas as pd


def create_graph(df: pd.DataFrame) -> plt.figure:
    """Создание графика распределения яркости."""
    brightness = df['Brightness_range']

    fig, ax = plt.subplots(figsize=(12, 6)) 
    ax.hist(brightness, bins=15, alpha=0.7, color='skyblue', edgecolor='black')

    mean_val = brightness.mean()
    median_val = brightness.median()

    ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Среднее: {mean_val:.1f}')
    ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Медиана: {median_val:.1f}')
    
    ax.set_title('Распределение диапазонов яркости изображений')
    ax.set_xlabel('Диапазон яркости')
    ax.set_ylabel('Количество изображений')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    return fig


def save_dataframe_to_csv(df: pd.DataFrame, filename: str = 'brightness_analysis.csv') -> None:
    """Сохранение DataFrame в CSV файл."""
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"DataFrame сохранен в {filename}")


def save_plot_to_file(fig: plt.Figure, filename: str) -> None:
    """Сохранение графика в файл."""
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"График сохранен в {filename}")