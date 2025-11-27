import pandas


def df_sort(df: pandas.DataFrame, column: str) -> pandas.DataFrame:
    sorted_df = df.sort_values(by=column, ascending=True)
    return sorted_df.reset_index(drop=True)


def filter_by_area(
    df: pandas.DataFrame, min_area: int, max_area: int
) -> pandas.DataFrame:
    filtered = df[(df["area_average"] >= min_area) & (df["area_average"] <= max_area)]
    return filtered.reset_index(drop=True)
