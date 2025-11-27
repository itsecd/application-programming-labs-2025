import pandas
import matplotlib.pyplot as plt


def add_range_column(df: pandas.DataFrame) -> pandas.DataFrame:
    """функция распределения площадей"""
    min_area = df["area"].min()
    max_area = df["area"].max()
    range_size = (max_area - min_area) // 5
    area_ranges = []
    for i in df["area"]:
        start = (int(i) // range_size) * range_size
        end = start + range_size - 1
        area_ranges.append(f"{start}-{end}")
    df["area_range"] = area_ranges
    df.sort_values(by="area_range", ascending=True)
    return df


def make_histogram(df: pandas.DataFrame) -> None:
    """функция создания гистограммы"""
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 3, 1)
    range_counts = df["area_range"].value_counts()
    plt.bar(range_counts.index, range_counts.values)
    plt.xlabel("Area distribution", fontsize=11)
    plt.ylabel("Quantity of files", fontsize=11)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("histogram.jpg")
    plt.show()
