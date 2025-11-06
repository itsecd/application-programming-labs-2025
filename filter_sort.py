import pandas as pd


def filtering_values(
    df: pd.DataFrame, name: str, min_values: float, max_values: float
) -> pd.DataFrame:
    """
    функция для фильтрации по диапазону значений
    """
    filtering_df = df[(df[name] > min_values) & (df[name] < max_values)]
    return filtering_df


def sort_range(dataframe: pd.DataFrame, name: str) -> pd.DataFrame:
    """
    функция для сортировки по значениям
    """
    return dataframe.sort_values(by=name).reset_index(drop=True)
