import argparse
import csv

import cv2
import matplotlib.pyplot as plt
import pandas as pd


def create_data(paths: list) -> pd.DataFrame:
    """
    Создает DataFrame по анотации со столбцом Ширина
    """
    data = pd.DataFrame(paths, columns=["Абсолютный путь", "Относительный путь"])
    widths = get_width(paths)
    data["Ширина"] = widths
    return data


def filter_data(data: pd.DataFrame, value: int, equation: bool) -> pd.DataFrame:
    """
    реализует функцию фильтрации по столбцу Ширины:
    при equation - True возвращет все строки с шириной больше value,
    False - возвращет все строки с шириной меньше value
    """
    if equation:
        filtered = data[data["Ширина"] > value]
    else:
        filtered = data[data["Ширина"] < value]
    return filtered


def get_width(paths: list) -> list:
    """
    возращает массив из значений ширины изображений
    """
    widths = []
    for p in paths:
        image = cv2.imread(p[0])
        width = image.shape[1]
        widths.append(width)
    return widths


def read_csv(annotation: str) -> list:
    """
    возращает массив из значений абсолютных и относительных путей до изображений
    """
    paths = []
    with open(annotation, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            paths.append(row)
    return paths


def install_graphs(d: pd.DataFrame, s: pd.DataFrame, f: pd.DataFrame, path: str) -> None:
    """
    накладывает графики по DataFrame d, s и f, затем выводит их на экран и сохраняет их по path
    """
    plt.plot(d['Ширина'])
    plt.plot(s['Ширина'])
    plt.plot(f['Ширина'])
    plt.xlabel('Индекс')
    plt.ylabel('Ширина')
    plt.savefig(path)
    plt.show()


def save_datas(d: pd.DataFrame, s: pd.DataFrame, f: pd.DataFrame, paths: list) -> None:
    """
    сохраняет DataFrame d, s и f по путям paths
    """
    d.to_csv(paths[0], index=True)
    s.to_csv(paths[1], index=True)
    f.to_csv(paths[2], index=True)


def main():
    parser = argparse.ArgumentParser(
        description="")

    parser.add_argument("annotation", type=str, help="абсолютный путь до файла анотации")
    parser.add_argument("dataframe_paths", nargs=3, type=str, help="путь для установки измененого изображения")
    parser.add_argument("graph_path", type=str, help="размер нового изображения формата widthXheight")

    args = parser.parse_args()

    paths = read_csv(args.annotation)

    data = create_data(paths)

    sorted_d = data.sort_values("Ширина", ascending=False)  # уже существует функция сортировки
    filtered_d = filter_data(data, 500, True)

    save_datas(data, sorted_d, filtered_d, args.dataframe_paths)

    install_graphs(data, sorted_d, filtered_d, args.graph_path)


if __name__ == "__main__":
    main()