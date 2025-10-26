import argparse
import pandas as pd

from data_processor import add_amplitude_column, filter_by_amplitude, sort_by_amplitude
from utils import get_correct_csv_path
from visualiser import plot_audio


def parser_t() -> tuple[str, str, str, float]:
    """
    Позволяет через консоль запускать код с аргументами
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=str, help="Путь к CSV файлу")
    parser.add_argument("output_plot", type=str, help="Путь для графика")
    parser.add_argument("output_csv", type=str, help="Путь для CSV")
    parser.add_argument("alpha", type=float, help="Число для фильтрации")
    args = parser.parse_args()
    return args.source, args.output_plot, args.output_csv, args.alpha


def main():
    source, output_plot, output_csv, value = parser_t()

    dff = pd.read_csv(source)

    if "text" in dff.columns:
        dff.drop("text", axis=1, inplace=True)

    dff = add_amplitude_column(dff)

    filtered_df = filter_by_amplitude(dff, value)

    sorted_df = sort_by_amplitude(filtered_df, ascending=True)
    plot_audio(sorted_df, output_plot)

    output_csv = get_correct_csv_path(output_csv)
    sorted_df.to_csv(output_csv, index=False)
    print(f"✅ CSV сохранён в {output_csv}")


if __name__ == "__main__":
    main()
