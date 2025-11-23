import numpy
import cv2
import pandas as pd
import matplotlib.pyplot as plt 
from download_images import parse_args, download_images, create_annotation, FileIterator

def calc_brightness_range(img: numpy.ndarray) -> int:
    """Вычисление распределения диапазона яркости изображения по всем каналам""" 
    return (img.max() - img.min())

def add_col2df(df: pd.core.frame.DataFrame, col_name: str, img_iter: FileIterator, func) -> None:
    """Добавляет столбец к DataFrame'у"""
    df[col_name] = None; 
    for i, path in enumerate(img_iter):
        img = cv2.imread(path)
        df.loc[i, col_name] = func(img)

def main() -> None:
    args = parse_args()
    # pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)

    try:
        # download_images(args.output, args.keywords)
        create_annotation(args.output, args.annotation)
        img_iter = FileIterator(args.annotation)
        df = pd.read_csv(args.annotation)
        add_col2df(df, "brightness_range", img_iter, calc_brightness_range)

        print(df)
           
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
       