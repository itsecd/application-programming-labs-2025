import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import argparse

def puller(img1: str) -> np.ndarray:
    """
    Преобразование файла в картинку
    """
    res = cv2.imread(img1)
    if res is None:
        raise FileNotFoundError
    return res


def read_csv(filename: str) -> pd.DataFrame:
    """
    Считывает csv файл в DataFrame
    """
    try:
        if(not filename.endswith(".csv")):
            filename += ".csv"
        return pd.read_csv(filename)
    except Exception as e:
        raise Exception(f"Error reading {e}")


def col(df: pd.DataFrame, columns: list[str]) -> None:
    """
    Задает название колонкам
    """
    if len(df.columns) != len(columns):
        raise Exception("Error")
    df.columns = columns


def get_squares(df: pd.DataFrame)->list:
    """
    Считает площадь каждой картинки и возвращет имя
    """
    res = []
    for path in df.iloc[:, 1]:
        img = puller(path)
        res.append(img.shape[0]*img.shape[1])
    return res


def append_squares(df: pd.DataFrame, squares: list, name:str) -> None:
    """
    Создает колонку с заданным названием
    """
    df[name] = squares


def sort_df(df: pd.DataFrame, ) -> pd.DataFrame:
    """
    Сортировка по площади
    """
    res = df.sort_values("площадь")
    return res


def filter(df: pd.DataFrame, condition: bool) -> pd.DataFrame:
    """
    Фильтрация по заданному условию
    """
    res = df[condition]
    return res


def graphic(df: pd.DataFrame) -> plt.Figure:
    """
    Создание и вывод графика площадей
    """
    x = np.linspace(1, len(df), len(df))
    y = df["площадь"].values

    figure = plt.figure()
    plt.plot(x, y)
    plt.xlabel("index")
    plt.ylabel("square")
    plt.grid(True)
    plt.show()
    return figure


def save_to_jpg(filename: str, fig: plt.Figure) -> None:
    """
    сохранение картинки в формате jpg файла
    """
    if not filename.endswith('.png'):
        filename += '.png'
    fig.savefig(filename)


def save_to_csv(filename: str, df: pd.DataFrame) -> None:
    """
    сохранение картинки в формате csv файла
    """
    if not filename.endswith('.csv'):
        filename += '.csv'
    df.to_csv(filename)


def main():
    parser = argparse.ArgumentParser(description="Извлечение данных из файла на основе шаблонов.")
    parser.add_argument("--csv", "-c", default = "data", type = str, help = "Считываемый csv файл")
    parser.add_argument("--res1", "-r1", default = "df", type = str, help = "Записываемый csv файл")
    parser.add_argument("--res2", "-r2", default = "graphic", type = str, help = "Записываемый png файл")

    args = parser.parse_args()
    df = read_csv(args.csv)
    print(df.head())
    try:
        col(df, ["Абсолютный путь", "Относительный путь"])
    except Exception as e:
        print(f"Find exception: {e}")
    print(df.head())

    squares = get_squares(df)
    append_squares(df, squares, "площадь")
    print(df)

    df1 = sort_df(df)
    print(df1)

    df2 = filter(df1, df1["площадь"] > 100000)
    print(df2)

    figure = graphic(df)

    save_to_jpg(args.res2, figure)
    save_to_csv(args.res1, df)

if __name__ == "__main__":
    main()