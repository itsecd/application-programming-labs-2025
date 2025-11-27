import cv2
import pandas


def create_DataFrame(file_path: str) -> pandas.DataFrame:
    df = pandas.DataFrame(pandas.read_csv(file_path))
    df.columns = ["Absolute_file_path", "Relative_file_path"]
    return df


def area_distrib(df: pandas.DataFrame) -> pandas.DataFrame:
    df.insert(2, "area_average", None)
    for index, row in df.iterrows():
        path = row["Relative_file_path"]
        img = cv2.imread(path)
        if img is not None:
            height, width = img.shape[:2]
            area = height * width
            df.at[index, "area_average"] = area
    return df
