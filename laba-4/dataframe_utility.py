import pandas as pd


def sort_by_brightness(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sort DataFrame by brightness.
    :param df: DataFrame to sort.
    :return: Sorted DataFrame.
    """
    return df.sort_values(by="brightness", ascending=True)


def filter_by_brightness_range(df: pd.DataFrame, brightness_range: str) -> pd.DataFrame:
    """
    Filter DataFrame by brightness_range.
    :param df: DataFrame to filter.
    :param brightness_range: Filter parameter.
    :return: Filtered DataFrame.
    """
    mask = df['brightness_range'] == brightness_range
    return df[mask]
