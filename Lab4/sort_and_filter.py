import numpy
import pandas


def df_sort(df: pandas.DataFrame, column: str) -> None:
    df.sort_values(by="column", inplace=True)


