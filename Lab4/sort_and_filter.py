import pandas


def df_sort(df: pandas.DataFrame, column: str) -> pandas.DataFrame:
    """функция сортировки"""
    sorted_df = df.sort_values(by=column, ascending=True)
    return sorted_df.reset_index(drop=True)


def filter_by_area(
    df: pandas.DataFrame, min_area: int, max_area: int
) -> pandas.DataFrame:
    """функция фильтрации по значению"""
    filtered = df[(df["area"] >= min_area) & (df["area"] <= max_area)]
    return filtered.reset_index(drop=True)
