import argparse
import pandas as pd


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
    pass


def calc_area(img) -> int:
    """
    Площадь изображения
    """
    pass


def add_area_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавление колонки площади изображений
    """
    pass


def sort_by_area(df: pd.DataFrame) -> pd.DataFrame:
    """
    Сортировка DataFrame по площади изображений
    """
    pass


def filter_by_area(df: pd.DataFrame, min_a: int, max_a: int) -> pd.DataFrame:
    """
    Фильтрация DataFrame по диапазону площади изображений
    """
    pass


def plot_histogram(df: pd.DataFrame, save_path: str) -> None:
    """
    Построение и сохранение гистограммы площадей изображений
    """
    pass


def main():
    try:
        args = parse_args()
        pass

    except Exception as exc:
        print(f"Ошибка: {exc}")


if __name__ == "__main__":
    main()
