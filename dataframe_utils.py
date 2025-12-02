import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os
import numpy as np
from typing import Optional, Tuple


def create_dataframe_from_annotation(annotation_file: str) -> Optional[pd.DataFrame]:
    """
    Создает DataFrame из файла аннотации

    Args:
        annotation_file (str): Путь к CSV файлу аннотации

    Returns:
        pd.DataFrame: DataFrame с путями к файлам
    """
    try:
        df = pd.read_csv(annotation_file)
        return df
    except Exception as e:
        print(f"Ошибка чтения аннотации: {e}")
        return None


def create_dataframe_from_folder(folder_path: str) -> Optional[pd.DataFrame]:
    """
    Создает DataFrame из папки с изображениями

    Args:
        folder_path (str): Путь к папке с изображениями

    Returns:
        pd.DataFrame: DataFrame с путями к файлам
    """
    try:
        data = []
        parent_dir = os.path.abspath(os.path.join(folder_path, os.pardir))

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                absolute_path = os.path.abspath(file_path)
                relative_path = os.path.relpath(absolute_path, parent_dir)

                data.append(
                    {"absolute_path": absolute_path, "relative_path": relative_path}
                )

        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Ошибка создания DataFrame из папки: {e}")
        return None


def add_aspect_ratio_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавляет колонку с отношением сторон изображения

    Args:
        df (pd.DataFrame): Исходный DataFrame

    Returns:
        pd.DataFrame: DataFrame с добавленной колонкой aspect_ratio
    """
    aspect_ratios = []

    for idx, row in df.iterrows():
        try:
            with Image.open(row["absolute_path"]) as img:
                width, height = img.size
                # ширина к высоте
                aspect_ratio = round(width / height, 2)
                aspect_ratios.append(aspect_ratio)
        except Exception as e:
            print(f"Ошибка обработки {row['absolute_path']}: {e}")
            aspect_ratios.append(None)

    df["aspect_ratio"] = aspect_ratios
    return df


def add_aspect_ratio_bins_column(df: pd.DataFrame, bins: int = 5) -> pd.DataFrame:
    """
    Добавляет колонку с диапазонами отношений сторон для гистограммы

    Args:
        df (pd.DataFrame): DataFrame с колонкой aspect_ratio
        bins (int): Количество диапазонов

    Returns:
        pd.DataFrame: DataFrame с добавленной колонкой aspect_ratio_range
    """
    # Удаляем NaN
    df_clean = df.dropna(subset=["aspect_ratio"])

    if len(df_clean) == 0:
        print("Нет данных для создания диапазонов")
        return df

    # диапазоны
    min_ratio = df_clean["aspect_ratio"].min()
    max_ratio = df_clean["aspect_ratio"].max()

    # границы
    boundaries = np.linspace(min_ratio, max_ratio, bins + 1)

    # определение диапазона
    def get_ratio_range(ratio: float) -> str:
        for i in range(len(boundaries) - 1):
            if boundaries[i] <= ratio <= boundaries[i + 1]:
                return f"{boundaries[i]:.2f}-{boundaries[i + 1]:.2f}"
        return "Unknown"

    df["aspect_ratio_range"] = df["aspect_ratio"].apply(
        lambda x: get_ratio_range(x) if pd.notnull(x) else "Unknown"
    )

    return df


def sort_by_aspect_ratio(df: pd.DataFrame, ascending: bool = True) -> pd.DataFrame:
    """
    Сортирует DataFrame по отношению сторон

    Args:
        df (pd.DataFrame): DataFrame для сортировки
        ascending (bool): Порядок сортировки

    Returns:
        pd.DataFrame: Отсортированный DataFrame
    """
    return df.sort_values("aspect_ratio", ascending=ascending, na_position="last")


def filter_by_aspect_ratio(
    df: pd.DataFrame,
    min_ratio: Optional[float] = None,
    max_ratio: Optional[float] = None,
) -> pd.DataFrame:
    """
    Фильтрует DataFrame по диапазону отношений сторон

    Args:
        df (pd.DataFrame): DataFrame для фильтрации
        min_ratio (float): Минимальное отношение сторон
        max_ratio (float): Максимальное отношение сторон

    Returns:
        pd.DataFrame: Отфильтрованный DataFrame
    """
    filtered_df = df.copy()

    if min_ratio is not None:
        filtered_df = filtered_df[filtered_df["aspect_ratio"] >= min_ratio]

    if max_ratio is not None:
        filtered_df = filtered_df[filtered_df["aspect_ratio"] <= max_ratio]

    return filtered_df


def plot_aspect_ratio_histogram(df: pd.DataFrame, output_plot: str) -> None:
    """
    Строит гистограмму распределения отношений сторон

    Args:
        df (pd.DataFrame): DataFrame с данными
        output_plot (str): Путь для сохранения графика
    """
    df_clean = df.dropna(subset=["aspect_ratio"])

    if len(df_clean) == 0:
        print("Нет данных для построения графика")
        return

    plt.figure(figsize=(12, 6))
    plt.hist(
        df_clean["aspect_ratio"], bins=10, alpha=0.7, color="skyblue", edgecolor="black"
    )

    plt.xlabel("Отношение сторон (ширина/высота)")
    plt.ylabel("Количество изображений")
    plt.title("Гистограмма распределения отношений сторон изображений")
    plt.grid(True, alpha=0.3)

    # Добавляем среднее значение
    mean_ratio = df_clean["aspect_ratio"].mean()
    plt.axvline(
        mean_ratio,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Среднее: {mean_ratio:.2f}",
    )

    plt.legend()
    plt.tight_layout()
    plt.savefig(output_plot, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Гистограмма сохранена: {output_plot}")


def plot_aspect_ratio_sorted(df: pd.DataFrame, output_plot: str) -> None:
    """
    Строит график отношений сторон для отсортированных данных

    Args:
        df (pd.DataFrame): DataFrame с данными
        output_plot (str): Путь для сохранения графика
    """
    # NaN + sort
    df_clean = df.dropna(subset=["aspect_ratio"])
    df_sorted = sort_by_aspect_ratio(df_clean)

    if len(df_sorted) == 0:
        print("Нет данных для построения графика")
        return

    plt.figure(figsize=(12, 6))

    # sort hist
    plt.plot(
        range(len(df_sorted)),
        df_sorted["aspect_ratio"],
        marker="o",
        linestyle="-",
        linewidth=1,
        markersize=3,
    )

    plt.xlabel("Номер изображения (отсортированный)")
    plt.ylabel("Отношение сторон (ширина/высота)")
    plt.title("Отношения сторон изображений (отсортированные)")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_plot, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"График сохранен: {output_plot}")
