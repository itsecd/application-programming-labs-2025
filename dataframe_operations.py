import pandas as pd


def sort_by_brightness_range(dataframe, ascending=True):
    """Сортировка DataFrame по колонке 'brightness_range'."""
    return dataframe.sort_values('brightness_range', ascending=ascending)


def filter_by_brightness_range(dataframe, min_value=None, max_value=None):
    """Фильтрация DataFrame по диапазону яркости."""
    filtered_df = dataframe.copy()
    if min_value is not None:
        filtered_df = filtered_df[filtered_df['brightness_range'] >= min_value]
    if max_value is not None:
        filtered_df = filtered_df[filtered_df['brightness_range'] <= max_value]
    return filtered_df