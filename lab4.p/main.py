from __future__ import annotations
import sys

from data_io import load_annotation_csv, save_dataframe
from image_processing import (
    add_orientation_column,
    sort_by_orientation,
    filter_by_orientation,
)
from visualization import plot_orientation_histogram


def main() -> None:
    """Главная функция лабораторной работы."""

    input_csv = (
        r"C:\Users\Владелец\application-programming"
        r"\application-programming-labs-2025\lab2.p\bears.csv"
    )

    output_csv = "lab4_orientation.csv"
    hist_file = "orientation_hist.png"

    df = load_annotation_csv(input_csv)
    print("КОЛОНКИ CSV:", df.columns.tolist())

    df = add_orientation_column(df)

    df_sorted = sort_by_orientation(df)
    df_square = filter_by_orientation(df_sorted, "Square")

    print("Первые строки:")
    print(df_sorted[["absolute_path", "orientation"]].head())
    print("Количество квадратных изображений:", len(df_square))

    plot_orientation_histogram(df_sorted, output_path=hist_file)
    save_dataframe(df_sorted, output_csv)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Ошибка:", e, file=sys.stderr)
        sys.exit(1)
