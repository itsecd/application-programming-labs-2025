import argparse
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import soundfile as sf


def args_parse() -> argparse.Namespace:
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        prog="Data parser",
        description="Parsing data from file"
    )
    parser.add_argument("-f", "--file", type=str, help="Path to csv")
    parser.add_argument("-o", "--output", type=str, help="Path to save csv")
    parser.add_argument("-p", "--plot", type=str, help="Path to save the plot image")
    parser.add_argument(
        "--minimum",
        type=float,
        default=0,
        help="minimum amplitude for filtering"
    )
    parser.add_argument(
        "--maximum",
        type=float,
        default=40000,
        help="maximum amplitude for filtering"
    )

    return parser.parse_args()


def correct_csv(csv_path: str) -> str:
    """Проверяет существует ли .csv в пути/названии или нет."""
    match = re.search(r"\.csv$", csv_path)
    if match:
        return csv_path
    return csv_path + ".csv"


def add_amplitude(df: pd.DataFrame) -> pd.DataFrame:
    """Добавляет столбец range для каждого файла."""
    result_df = df.copy()

    for i, path in enumerate(result_df["relative_path"]):
        try:
            data, samplerate = sf.read(path)
            ampl = np.max(data) - np.min(data)
            result_df.loc[i, "range"] = ampl
        except Exception as e:
            print(f"Ошибка при чтении {path}: {e}")
            result_df.loc[i, "range"] = 0.0

    return result_df


def filter_amplitude(df: pd.DataFrame, min_val: int, max_val: int) -> pd.DataFrame:
    """Фильтрует DataFrame по range принадлежащих [min, max]."""
    df["range"] = pd.to_numeric(df["range"], errors='coerce')
    filter_df = df[
        (df["range"] >= min_val) & (df["range"] <= max_val)
    ].reset_index(drop=True)
    return filter_df


def sort_amplitude(df: pd.DataFrame) -> pd.DataFrame:
    """Сортирует DataFrame по range."""
    sort_df = df.sort_values("range", ascending=True).reset_index(drop=True)
    return sort_df


def plot_audio(df: pd.DataFrame, path: str) -> None:
    """График данных."""
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["range"], color="blue")
    plt.title("График для амлитуды от аудиофайла")
    plt.xlabel("Номер аудиофайла")
    plt.ylabel("Амплитуда")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()


def main():
    """Основная функция программы."""
    args = args_parse()

    if not args.file:
        print("Please specify file using -f argument")
        return

    if not args.output:
        print("Please specify output using -o argument")
        return

    if not args.plot:
        print("Please specify plot audio using -p argument")
        return

    min_val = args.minimum
    max_val = args.maximum

    columns_name = ["name", "absolute_path", "relative_path", "range"]
    df = pd.read_csv(args.file, header=None, names=columns_name)
    df = add_amplitude(df)
    filter_df = filter_amplitude(df, min_val, max_val)
    sort_df = sort_amplitude(filter_df)
    plot_audio(sort_df, args.plot)

    output_csv = correct_csv(args.output)
    sort_df.to_csv(output_csv, index=False)


if __name__ == "__main__":
    main()