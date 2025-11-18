import argparse

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
    parser = argparse.ArgumentParser(description="создает датафреймы и реализует их сортировку и сохранение полученых датафреймов и графиков на их основе")

    parser.add_argument("annotation", type=str, help="абсолютный путь до файла анотации")
    parser.add_argument("dataframe_paths", nargs=3, type=str, help="пути для установки полученых датафреймов(3)")
    parser.add_argument("graph_paths", nargs=3, type=str, help="пути для сохранения графиков")

    return parser


def get_widths(paths: list) -> list:
    """
    возращает массив из значений ширины изображений
    """
    widths = []
    for path in paths:
        image = cv2.imread(path)
        width = image.shape[1]
        widths.append(width)
    return widths


def create_data(path: str) -> pd.DataFrame:
    """
    Создает DataFrame по аннотации
    """
    column_names = ['Абсолютеный путь', 'Относительный путь']

    df = pd.read_csv(path, names=column_names, header=None)

    return df


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


def install_graphs(df: pd.DataFrame, path: str) -> None:
    """
    накладывает графики по DataFrame d, s и f, затем выводит их на экран и сохраняет их по path
    """
    plt.plot(df['Ширина'])

    plt.xlabel('Индекс')
    plt.ylabel('Ширина')

    plt.savefig(path)
    plt.show()
