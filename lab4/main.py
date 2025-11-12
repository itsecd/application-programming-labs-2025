import os
import argparse

import numpy as np
import pandas as pd
import soundfile as sf
import matplotlib.pyplot as plt

from track_iterator import TrackIterator


def compute_amplitude_range(file_path: str) -> float:
    data, sr = sf.read(file_path)
    return float(np.max(data) - np.min(data))


def build_dataframe(source: str) -> pd.DataFrame:
    abs_paths, rel_paths, ranges = [], [], []

    for path in TrackIterator(source):
        abs_paths.append(path)
        rel_paths.append(os.path.relpath(path))
        ranges.append(compute_amplitude_range(path))

    df = pd.DataFrame({
        "absolute": abs_paths,
        "relative": rel_paths,
        "amplitude(range)": ranges
    })
    return df


def sort_by_amplitude(df: pd.DataFrame, ascending: bool = True) -> pd.DataFrame:
    return df.sort_values(by="amplitude(range)", ascending=ascending)


def filter_by_amplitude(df: pd.DataFrame, min_value: float, max_value: float) -> pd.DataFrame:
    return df[(df["amplitude(range)"] >= min_value) & (df["amplitude(range)"] <= max_value)]


def plot_histogram(df: pd.DataFrame, output_path: str):
    plt.figure(figsize=(8, 5))
    plt.hist(df["amplitude(range)"], bins=10, edgecolor="black", align="left")
    plt.title("Гистограмма распределения диапазона амплитуды")
    plt.xlabel("Диапазон амплитуды (range)")
    plt.ylabel("Количество файлов")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="path/to/csv/file")
    parser.add_argument("-o", "--output", default="./result", help="path/to/result/folder")
    parser.add_argument("--min", type=float, default=-100.0, help="hist filter: min value")
    parser.add_argument("--max", type=float, default=+100.0, help="hist filter: max value")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise FileNotFoundError(f"File or dir {args.input} not found.")
    os.makedirs(args.output, exist_ok=True)
    return args


def main():
    args = parse_args()

    df = build_dataframe(args.input)

    if args.min is not None or args.max is not None:
        df = filter_by_amplitude(df, args.min, args.max)

    df_sorted = sort_by_amplitude(df)

    csv_output = os.path.join(args.output, "sorted_data.csv")
    img_output = os.path.join(args.output, "amplitude_distribution.png")

    df_sorted.to_csv(csv_output, index=False)
    plot_histogram(df_sorted, output_path=img_output)

    print(f"✅ CSV save: {csv_output}")
    print(f"✅ hist pic save: {img_output}")


if __name__ == "__main__":
    main()

