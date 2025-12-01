from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

def load_paths_dataframe(csv_path: Path) -> pd.DataFrame:
    """
    Загрузка DataFrame из CSV-файла аннотации ЛР2.
    """
    df = pd.read_csv(csv_path)
    df = df.rename(columns={"absolute_path": "absolute_path", "relative_path": "relative_path"})
    return df

def calculate_brightness(image_path: str) -> float:
    """
    Вычисление средней яркости изображения по всем каналам.
    """
    image = Image.open(image_path).convert("RGB")
    array = np.array(image)
    brightness = float(array.mean())
    return brightness

def add_brightness_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавление в DataFrame колонку avg_brightness с яркостью.
    """
    df["avg_brightness"] = df["absolute_path"].apply(
        calculate_brightness
    )
    return df

def sort_by_brightness(df: pd.DataFrame) -> pd.DataFrame:
    """
    Сортировка строки DataFrame по средней яркости.
    """
    sorted_df = df.sort_values(by="avg_brightness", ascending=True)
    return sorted_df

def filter_by_brightness(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """
    Фильтрация DataFrame по яркости: оставляет ярче порога.
    """
    filtered_df = df[df["avg_brightness"] > threshold]
    return filtered_df

def plot_brightness(df: pd.DataFrame, png_path: Path) -> None:
    """
    Построение и сохранение графика средней яркости изображений.
    """
    x_values = range(len(df))
    y_values = df["avg_brightness"].tolist()

    plt.figure(figsize=(8, 4))
    plt.plot(x_values, y_values, marker="o")
    plt.title("Средняя яркость изображений")
    plt.xlabel("Номер изображения")
    plt.ylabel("Яркость (0–255)")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(png_path)
    plt.close()

def save_dataframe(df: pd.DataFrame, csv_path: Path) -> None:
    """
    Сохранение DataFrame в CSV файл.
    """
    df.to_csv(csv_path, index=False)

def main() -> None:
    """
    Главная функция
    """
    # путь к CSV из ЛР2
    annotation_csv = Path("annotation.csv")

    # загрузка данных и формирование DataFrame
    df_paths = load_paths_dataframe(annotation_csv)

    # добавление колонки по варианту (средняя яркость)
    df_with_brightness = add_brightness_column(df_paths)

    # сортировка по новой колонке
    df_sorted = sort_by_brightness(df_with_brightness)

    # фильтрация
    mean_brightness = float(df_sorted["avg_brightness"].mean())
    df_filtered = filter_by_brightness(df_sorted, mean_brightness)

    # построение графика по отсортированным данным
    plot_brightness(
        df_sorted,
        png_path=Path("brightness_plot.png"),
    )

    # сохранение итогового dataframe и графика
    save_dataframe(df_filtered, csv_path=Path("result.csv"))


if __name__ == "__main__":
    main()