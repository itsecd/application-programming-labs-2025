import argparse
import csv

import cv2
import matplotlib.pyplot as plt
import pandas as pd


def csv_check(path: str, paths: list) -> None:
    """
    провереяет первые 4 аргумента на csv файл
    """
    paths.append(path)
    for path in paths:
        if path[-4:] != '.csv':
            raise ValueError(f'{path} должен содержать csv файл')


def parsing() -> argparse.ArgumentParser:
    """
    осушествляет парсинг аргументов
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("annotation", type=str, help="абсолютный путь до файла анотации")
    parser.add_argument("dataframe_paths", nargs=3, type=str, help="путь для установки измененого изображения")
    parser.add_argument("graph_path", type=str, help="размер нового изображения формата widthXheight")

    return parser


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


def get_width(paths: list) -> list:
    """
    возращает массив из значений ширины изображений
    """
    widths = []
    for path in paths:
        if len(path) != 2:
            raise ValueError('файл аннотации не подходит шаблону [абсолютный путь, относительный путь]')
        image = cv2.imread(path[0])
        width = image.shape[1]
        widths.append(width)
    return widths


def create_data(paths: list) -> pd.DataFrame:
    """
    Создает DataFrame по аннотации со столбцом Ширина
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


def save_datas(d: pd.DataFrame, s: pd.DataFrame, f: pd.DataFrame, paths: list) -> None:
    """
    сохраняет DataFrame d, s и f по путям paths
    """
    d.to_csv(paths[0], index=True)
    s.to_csv(paths[1], index=True)
    f.to_csv(paths[2], index=True)


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


def main():
    try:
        parser = parsing()
        args = parser.parse_args()

        csv_check(args.annotation, args.dataframe_paths)

        paths = read_csv(args.annotation)

        data = create_data(paths)

        sorted_d = data.sort_values("Ширина", ascending=False)  # уже существует функция сортировки
        filtered_d = filter_data(data, 500, True)

        save_datas(data, sorted_d, filtered_d, args.dataframe_paths)

        install_graphs(data, sorted_d, filtered_d, args.graph_path)

    except ValueError as e:
        print(e)
    except cv2.error as e:
        print(e)


if __name__ == "__main__":
    main()