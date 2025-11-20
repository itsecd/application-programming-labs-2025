import os

import cv2
import numpy as np
import pandas


def create_DataFrame(file_path: str) -> pandas.DataFrame:
    df = pandas.DataFrame(pandas.read_csv(file_path))
    df.columns = ["Absolute_file_path", "Relative_file_path"]
    return df


def area_distrib(df:pandas.DataFrame) -> None:
    df.insert(2,"area_average", None)
    for i in os.listdir("dogs"):
        path = os.path.join("dogs", i)
        img = cv2.imread(path)
        shape = img.shape
        area = shape[0]*shape[1]
        df["area_average"] = area