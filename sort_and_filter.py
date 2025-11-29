import pandas as pd

def sort_dataframe_by_brightness(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Сортирование DataFrame по указанной колонке яркости
    :param df: сформированный DataFrame с добавленными колонками
    :param column_name: колонка яркости
    :return: отсортированный DataFrame по указанной колонке яркости
    """
    df_sorted = df.sort_values(by=column_name, ascending=True).reset_index(drop=True)

    return df_sorted

def filter_dataframe_by_brightness(df: pd.DataFrame, min_val: int, max_val: int, column_name: str) -> pd.DataFrame:
    """
    Фильтрация DataFrame, оставляя только изображения, где значение яркости
    в колонке column_name находится в диапазоне [min_val, max_val].
    :param df: Сформированный DataFrame
    :param min_val: Минимальное значение яркости
    :param max_val: Максимальное значение яркости
    :param column_name: Колонка канала яркости
    :return: Отфильтрованный DataFrame
    """
    mask = (df[column_name] >= min_val) & (df[column_name] <= max_val)
    df_filtered = df[mask]

    return df_filtered