import sys
import argparse

from data_io import load_annotation_csv, save_dataframe
from image_processing import (
    add_orientation_column,
    sort_by,
    filter_by_orientation,
)
from visualization import plot_orientation_histogram


def parse_args() -> argparse.Namespace:
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Обработка изображений и анализ ориентации."
    )

    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Путь к входному CSV файлу с аннотациями",
    )

    parser.add_argument(
        "--output",
        "-o",
        default="lab4_orientation.csv",
        help="Путь к файлу для сохранения результата (CSV)",
    )

    parser.add_argument(
        "--hist",
        "-H",
        default="orientation_hist.png",
        help="Файл для сохранения гистограммы ориентаций",
    )

    return parser.parse_args()


def main() -> None:
    """Главная функция лабораторной работы."""
    args = parse_args()

    try:
        df = load_annotation_csv(args.input)
        print("КОЛОНКИ CSV:", df.columns.tolist())

        df = add_orientation_column(df)

        df_sorted = sort_by(df)
        df_square = filter_by_orientation(df_sorted, "Square")

        print("Первые строки:")
        print(df_sorted[["absolute_path", "orientation"]].head())
        print("Количество квадратных изображений:", len(df_square))

        plot_orientation_histogram(df_sorted, output_path=args.hist)
        save_dataframe(df_sorted, args.output)

    except Exception as e:
        print("Ошибка:", e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
