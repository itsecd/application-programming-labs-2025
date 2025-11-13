import os

import cv2
import pandas as pd
import numpy as np


def create_DataFrame(data_file_name: str) -> pd.DataFrame:
    """
    Создание dataFrame и переименование колонок
    """
    df = pd.DataFrame(pd.read_csv(data_file_name))
    df.columns = ["Absolute_file_path", "Relative_file_path"]
    return df


def distribution_brightness_columns(df: pd.DataFrame) -> None:
    """
    Добавление колонок со значениями распределения яркости
    """
    blue_average = []
    red_average = []
    green_average = []
    df.insert(2, "Red_average", None)
    df.insert(3, "Green_average", None)
    df.insert(4, "Blue_average", None)
    for f in os.listdir("images"):
        path = os.path.join("images", f)
        img = cv2.imread(path)
        b, g, r = cv2.split(img)
        blue_average.append(np.mean(b))
        red_average.append(np.mean(r))
        green_average.append(np.mean(g))
    df["Blue_average"] = blue_average
    df["Green_average"] = green_average
    df["Red_average"] = red_average
