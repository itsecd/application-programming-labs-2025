import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import argparse


def load_dataset(path):
    """
    загрузка датасета
    """
    return pd.read_csv(path)


def compute_brightness(path):
    """
    вычисление яркости
    """
    try:
        img = Image.open(path).convert("L")
        arr = np.array(img)
        return float(arr.mean())
    except:
        return float("nan")


def add_brightness_column(df):
    """
    добавление колонки с яркостью
    """
    df["brightness"] = df["absolute_path"].apply(compute_brightness)
    return df


def sort_by_brightness(df):
    """
    сортировка
    """
    return df.sort_values(by="brightness")



def plot_histogram(df, step, output="brightness_histogram.png"):
    """
    построение гистограммы с подписями диапазонов
    """
    brightness_values = df["brightness"].dropna()

    max_val = 256
    bins = list(range(0, max_val, step)) + [255]

    labels = [str(bins[i]) for i in range(len(bins)-1)]

    plt.figure(figsize=(12, 6))

    counts, _, _ = plt.hist(brightness_values, bins=bins)

    plt.xticks(
        [bins[i] for i in range(len(bins)-1)],
        labels,
        rotation=0
    )

    plt.xlabel("Диапазон яркости")
    plt.ylabel("Количество изображений")
    plt.title(f"Гистограмма распределения яркости (шаг={step})")
    plt.tight_layout()

    plt.savefig(output)
    plt.close()


def check_range(value):
    ivalue = int(value)
    if 8 <= ivalue <= 256:
        return ivalue
    else:
        print( f"значение должно быть от 8 до 256, получено {ivalue}. используется значение по умолчанию")
        return 16

def main():
    parser = argparse.ArgumentParser(description="histogram lab")
    parser.add_argument("--range", type=check_range, default=16,
                        help="размер диапазона яркости для гистограммы (например 16)")

    args = parser.parse_args()
    step = args.range

    df = load_dataset("dataset_lab2.csv")

    df = add_brightness_column(df)

    df_sorted = sort_by_brightness(df)

    plot_histogram(df_sorted, step=step)

    df_sorted.to_csv("result_dataframe.csv", index=False)

    print(f"шаг диапазона = {step}")
    print("сохранено: result_dataframe.csv, brightness_histogram.png")


if __name__ == "__main__":
    main()
