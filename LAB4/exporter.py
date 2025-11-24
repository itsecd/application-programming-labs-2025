import pandas as pd
import matplotlib.pyplot as plt
from typing import Union


def save_dataframe(df: pd.DataFrame, base_filename: str) -> None:
    """
    Сохраняет DataFrame в CSV и Excel файлы
    
    Args:
        df: DataFrame для сохранения
        base_filename: Базовое имя файла (без расширения)
    """
    df.to_csv(f'{base_filename}.csv', index=False, encoding='utf-8')
    df.to_excel(f'{base_filename}.xlsx', index=False)


def save_plot(plot: plt.Figure, filename: str, dpi: int = 300) -> None:
    """
    Сохраняет график в файл
    
    Args:
        plot: Объект Figure для сохранения
        filename: Имя файла
        dpi: Разрешение для сохранения
    """
    plot.savefig(filename, dpi=dpi, bbox_inches='tight')
    plot.show()