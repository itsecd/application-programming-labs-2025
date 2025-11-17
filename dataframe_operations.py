import pandas as pd
from pandas import DataFrame


def sort_by_brightness_range(dataframe: DataFrame, ascending: bool = True) -> DataFrame:
    """Сортировка DataFrame по колонке 'brightness_range'."""
    return dataframe.sort_values('brightness_range', ascending=ascending)


def filter_by_brightness_range(
    dataframe: DataFrame, 
    min_value: float | None = None, 
    max_value: float | None = None
) -> DataFrame:
    """Фильтрация DataFrame по диапазону яркости."""
    filtered_df = dataframe.copy()
    if min_value is not None:
        filtered_df = filtered_df[filtered_df['brightness_range'] >= min_value]
    if max_value is not None:
        filtered_df = filtered_df[filtered_df['brightness_range'] <= max_value]
    return filtered_df