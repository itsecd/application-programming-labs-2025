import pandas as pd


def save_dataframe(dataframe: pd.DataFrame, fail_save_data: str) -> None:
    """
    функция для сохранения dataframe  в файл
    """
    dataframe.to_csv(fail_save_data)
