import pandas as pd


def creating_dataframe_and_columns(fail: str) -> pd.DataFrame:
    """
    функция для создания dataframe и создания в нем заголовков
    """
    dataframe = pd.read_csv(fail, names=["absolute_path", "relative_path"], skiprows=1)
    dataframe = dataframe.rename(
        columns={
            "absolute_path": "Абсолютный путь",
            "relative_path": "Относительный путь",
        }
    )
    return dataframe
