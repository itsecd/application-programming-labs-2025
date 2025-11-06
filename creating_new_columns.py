import cv2
import pandas as pd


def creating_range_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    функция для создания трех новыйх колонок по разнице яркости каждого канала
    """
    dataframe["range_r"] = 0.0
    dataframe["range_g"] = 0.0
    dataframe["range_b"] = 0.0
    for idx in dataframe.index:
        value = dataframe.loc[idx, "Абсолютный путь"]
        img = cv2.imread(value)
        range_b = img[:, :, 0].max() - img[:, :, 0].min()
        range_g = img[:, :, 1].max() - img[:, :, 1].min()
        range_r = img[:, :, 2].max() - img[:, :, 2].min()
        dataframe.at[idx, "range_r"] = range_r
        dataframe.at[idx, "range_g"] = range_g
        dataframe.at[idx, "range_b"] = range_b
    return dataframe
