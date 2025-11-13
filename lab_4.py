import os

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def create_DataFrame() -> pd.DataFrame:
    """
    Создание dataFrame и переименование колонок
    """
    df = pd.DataFrame(pd.read_csv("data.csv"))
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


def sorted_graph(df: pd.DataFrame) -> None:
    """
    Отоображение отсортированного графа
    """
    df_sorted_red = df.sort_values(by="Red_average", ascending=True)
    df_sorted_green = df.sort_values(by="Green_average", ascending=True)
    df_sorted_blue = df.sort_values(by="Blue_average", ascending=True)
    x = range(len(df_sorted_blue["Blue_average"]))
    plt.plot(x, df_sorted_blue["Blue_average"], color="blue")
    plt.plot(x, df_sorted_red["Red_average"], color="red")
    plt.plot(x, df_sorted_green["Green_average"], color="green")
    plt.xlabel("Number of image")
    plt.ylabel("Average brightness")
    plt.title("Sorted data")
    plt.savefig("sorted_data.png")
    plt.show()


def get_brightness_range(value: float) -> str:
    """
    Вспомогательная функция для создания колонок с диапозоном для гистограммы
    """
    if value < 50:
        return "0-49"
    elif value < 100:
        return "50-99"
    elif value < 150:
        return "100-149"
    elif value < 200:
        return "150-199"
    else:
        return "200-255"


def make_histogram(df: pd.DataFrame) -> None:
    """
    Функция создания гистограммы
    """
    df_1 = df.copy()
    df_1["Brightness_range_blue"] = df_1["Blue_average"].apply(get_brightness_range)
    df_1["Brightness_range_green"] = df_1["Green_average"].apply(get_brightness_range)
    df_1["Brightness_range_red"] = df_1["Red_average"].apply(get_brightness_range)
    range_counts_blue = df_1["Brightness_range_blue"].value_counts()
    range_counts_green = df_1["Brightness_range_green"].value_counts()
    range_counts_red = df_1["Brightness_range_red"].value_counts()
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 3, 1)
    plt.bar(range_counts_blue.index, range_counts_blue.values, color="blue")
    plt.xlabel("Brightness ranges")
    plt.ylabel("Quantity of files")
    plt.title("Distribution")
    plt.subplot(1, 3, 2)
    plt.bar(range_counts_red.index, range_counts_red.values, color="red")
    plt.xlabel("Brightness ranges")
    plt.ylabel("Quantity of files")
    plt.title("Distribution")
    plt.subplot(1, 3, 3)
    plt.bar(range_counts_green.index, range_counts_green.values, color="green")
    plt.xlabel("Brightness ranges")
    plt.ylabel("Quantity of files")
    plt.title("Distribution")
    plt.savefig("histogram.png")
    plt.show()


def main() -> None:
    try:
        df = create_DataFrame()
        distribution_brightness_columns(df)
        filters = {"red_min": 123}
        filter(filters, df)
        sorted_graph(df)
        make_histogram(df)
        df.to_csv("dataframe.csv")
    except Exception as exp:
        print(exp)


if __name__ == "__main__":
    main()
