import argparse
import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt


def rang_calculate(path: str) -> int:
    """Вычисление диапазона яркости"""
    img = cv2.imread(path)
    height, width, channels = img.shape
    max=-1
    min=256
    for i in range(height):
        for j in range(width):
            for k in range(3):
                if max<img[i,j,k]:
                    max = img[i,j,k]
                if min>img[i,j,k]:
                    min = img[i,j,k]
    return max-min

def sort_by_brightness_range(df: pd.DataFrame) -> pd.DataFrame:
    """Сортировка таблички"""
    return df.sort_values(by="brightness range")

def filter_by_brightness_range(df: pd.DataFrame, value: int) -> pd.DataFrame:
    """Фильтрация таблички по заданному значению"""
    return df[df["brightness range"] > value].reset_index(drop=True)

def parse_arguments():
    """Парсинг аргументов"""
    parser = argparse.ArgumentParser(description='Работа с pandas')
    parser.add_argument(
        '--input_csv',
        required=True,
        help='Исходный файл с путями'
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    name = args.input_csv
    df = pd.read_csv(name)
    df['brightness range'] = 0
    for i in range(len(df)):
        df.iloc[i,2] = rang_calculate(df.iloc[i,1])
    df = sort_by_brightness_range(df)
    plot_brightness(df)
    df = filter_by_brightness_range(df, 250)
    print(df)
    df.to_csv('data.csv', index=False)


def plot_brightness(df: pd.DataFrame) -> None:
    """Vizualizated and save DataFrame by plt"""
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(df)), df.iloc[:, 2], marker='o', linewidth=2, markersize=4)
    plt.title('Диапазон яркости по изображениям')
    plt.xlabel('Номер изображения')
    plt.ylabel('Диапазон яркости')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('brightness_plot.png')
    plt.show()

if __name__ == "__main__":
    main()