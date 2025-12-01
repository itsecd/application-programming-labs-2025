import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import cv2


def parse_args():
    parser = argparse.ArgumentParser(description="Лабораторная работа №4")

    parser.add_argument(
        "annotation",
        type=str,
        help="Путь к CSV-файлу аннотации из ЛР2"
    )
    parser.add_argument(
        "output_df",
        type=str,
        help="Путь для сохранения итогового DataFrame"
    )
    parser.add_argument(
        "output_plot",
        type=str,
        help="Путь для сохранения гистограммы"
    )

    parser.add_argument(
        "--min_area",
        type=int,
        default=0,
        help="Минимальная площадь изображения для фильтрации"
    )

    parser.add_argument(
        "--max_area",
        type=int,
        default=10**12,
        help="Максимальная площадь изображения для фильтрации"
    )

    return parser.parse_args()


def load_annotation(annotation_path: str) -> pd.DataFrame:
    """
    Загрузка CSV с абсолютными и относительными путями
    """
    if not os.path.exists(annotation_path):
        raise FileNotFoundError("Файл аннотации не найден")

    df = pd.read_csv(annotation_path)
    df.columns = ["absolute_path", "relative_path"]
    return df


def calc_area(img):
    """
    Площадь изображения
    """
    h, w = img.shape[:2]
    return h * w


def add_area_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавление колонки площади изображений
    """
    df["area"] = None

    for i, path in enumerate(df["absolute_path"]):
        if not os.path.isfile(path):
            df.loc[i, "area"] = 0
            continue

        img = cv2.imread(path)
        if img is None:
            df.loc[i, "area"] = 0
            continue

        df.loc[i, "area"] = calc_area(img)

    return df


def sort_by_area(df: pd.DataFrame) -> pd.DataFrame:
    """
    Сортировка DataFrame по площади изображений
    """
    return df.sort_values("area", ascending=True)


def filter_by_area(df: pd.DataFrame, min_a: int, max_a: int) -> pd.DataFrame:
    """
    Фильтрация DataFrame по диапазону площади изображений
    """
    return df[(df["area"] >= min_a) & (df["area"] <= max_a)]


def plot_histogram(df: pd.DataFrame, save_path: str):
    """
    Построение и сохранение гистограммы площадей изображений
    """
    plt.hist(df["area"], bins=20)

    plt.title("Гистограмма распределения площадей изображений")
    plt.xlabel("Площадь изображения (в пикселях)")
    plt.ylabel("Количество изображений")

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()


def main():
    args = parse_args()

    try:
        df = load_annotation(args.annotation)

        df = add_area_column(df)

        df = sort_by_area(df)

        df = filter_by_area(df, args.min_area, args.max_area)

        plot_histogram(df, args.output_plot)

        df.to_csv(args.output_df, index=False, encoding="utf-8")

        print("Сохранённый DataFrame:", args.output_df)
        print("Сохранённая гистограмма:", args.output_plot)

    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()
