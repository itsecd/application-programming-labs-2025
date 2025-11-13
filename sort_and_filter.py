import pandas as pd


def sort_columns(name_column: str, df: pd.DataFrame) -> None:
    """
    Сортировка колонок
    """
    df.sort_values(by=name_column, ascending=True, inplace=True)


def filter(filters: dict, df: pd.DataFrame) -> None:
    """
    Фильтрация колонок
    """
    for key, value in filters.items():
        if key == "red_min":
            df = df[df["Red_average"] >= value]
        if key == "red_max":
            df = df[df["Red_average"] <= value]
        if key == "blue_min":
            df = df[df["Blue_average"] >= value]
        if key == "blue_max":
            df = df[df["Blue_average"] <= value]
        if key == "green_min":
            df = df[df["Green_average"] >= value]
        if key == "green_max":
            df = df[df["Green_average"] <= value]
