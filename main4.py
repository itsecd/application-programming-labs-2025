import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from typing import Any
from PIL import Image
import matplotlib
matplotlib.use('Agg')


def load_annotation(csv_path: str = "annotation.csv") -> pd.DataFrame:
    """
    Загружает аннотацию из CSV-файла.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Файл аннотации не найден: {csv_path}")
    df = pd.read_csv(csv_path)
    if df.empty:
        raise ValueError("Файл аннотации пуст.")
    return df


def get_image_size(file_path: str) -> tuple[int, int]:
    """
    Получает ширину и высоту изображения.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Изображение не найдено: {file_path}")

    try:
        with Image.open(file_path) as img:
            return img.width, img.height
    except Exception as e:
        raise ValueError(f"Не удалось открыть изображение '{file_path}': {e}")


def add_image_dimensions(df: pd.DataFrame, path_col: str = "Absolute Path") -> pd.DataFrame:
    """
    Добавляет колонки 'Ширина', 'Высота' и 'Отношение сторон'
    """
    print("Получаем размеры изображений...")

    widths = []
    heights = []

    for idx, row in df.iterrows():
        file_path = row[path_col]
        try:
            w, h = get_image_size(file_path)
            widths.append(w)
            heights.append(h)
            print(f"   [{idx + 1}/{len(df)}] {os.path.basename(file_path)}: {w}x{h}")
        except Exception as e:
            print(f"Ошибка для {file_path}: {e}")
            widths.append(0)
            heights.append(0)

    df['Ширина'] = widths
    df['Высота'] = heights

    if (df['Ширина'] == 0).any():
        print("Найдены изображения с шириной = 0. Они будут пропущены в расчёте отношения.")

    df['Отношение сторон (длина/ширина)'] = df['Высота'] / df['Ширина']
    df['Отношение сторон (длина/ширина)'] = df['Отношение сторон (длина/ширина)'].replace([float('inf'), float('-inf')], 0)

    return df


def sort_and_filter(df: pd.DataFrame, sort_col: str = 'Отношение сторон (длина/ширина)',
    min_ratio: float = 0.7, max_ratio: float = 1.5
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Сортирует и фильтрует DataFrame по отношению сторон.
    """
    df_sorted = df.sort_values(by=sort_col).reset_index(drop=True)
    df_filtered = df_sorted[
        (df_sorted[sort_col] >= min_ratio) & (df_sorted[sort_col] <= max_ratio)
    ].reset_index(drop=True)
    return df_sorted, df_filtered


def plot_histogram(df: pd.DataFrame, output: str = "aspect_ratio_histogram.png") -> None:
    """
    Строит и сохраняет гистограмму распределения отношений сторон.
    """
    bins = [0, 0.8, 1.2, 1.6, 2.0, float("inf")]
    labels = ["0–0.8", "0.81–1.2", "1.21–1.6", "1.61–2.0", ">2.0"]

    df['Диапазон'] = pd.cut(df['Отношение сторон (длина/ширина)'], bins=bins, labels=labels, right=False)
    hist_data = df['Диапазон'].value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    bars = plt.bar(hist_data.index, hist_data.values, color="skyblue", edgecolor="black")
    plt.title("Гистограмма распределения отношений сторон изображений")
    plt.xlabel("Диапазон (высота / ширина)")
    plt.ylabel("Количество изображений")
    plt.grid(True, alpha=0.3)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, int(height),
                 ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Гистограмма сохранена: {output}")


def save_result(df: pd.DataFrame, path: str = "sorted_images_data.csv") -> None:
    """
    Сохраняет результат в CSV.
    """
    df.to_csv(path, index=False, encoding='utf-8-sig')
    print(f"Таблица сохранена: {path}")


def main() -> None:
    df = load_annotation("annotation.csv")

    df = add_image_dimensions(df, path_col="Absolute Path")

    df_sorted, df_filtered = sort_and_filter(df)

    plot_histogram(df_sorted)

    save_result(df_sorted)

    print(f"Всего изображений: {len(df_sorted)}")
    print(f"После фильтрации (0.7–1.5): {len(df_filtered)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)