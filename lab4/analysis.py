import os
import argparse

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import soundfile as sf


def get_args() -> argparse.Namespace:
    """Разбор аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Анализ аудиотреков: построение DataFrame, сортировка, фильтрация, графики."
    )
    parser.add_argument(
        "-a", "--annotation_csv",
        type=str,
        default=os.path.join("downloads", "annotation.csv"),
        help="CSV-файл с аннотацией аудиотреков"
    )
    parser.add_argument(
        "-o", "--output_dir",
        type=str,
        default="analysis",
        help="Папка для сохранения всех результатов анализа"
    )
    parser.add_argument(
        "-d", "--dataframe_dir",
        type=str,
        default=os.path.join("analysis", "dataframe"),
        help="Папка для сохранения датафреймов"
    )
    parser.add_argument(
        "-g", "--graphics_dir",
        type=str,
        default=os.path.join("analysis", "graphics"),
        help="Папка для сохранения графиков"
    )
    
    args = parser.parse_args()

    args.annotation_csv = os.path.normpath(args.annotation_csv)
    args.output_dir = os.path.normpath(args.output_dir)
    args.dataframe_dir = os.path.normpath(args.dataframe_dir)
    args.graphics_dir = os.path.normpath(args.graphics_dir)

    return args


def read_audio_mean_amplitude(filepath: str) -> float:
    """Вычисляет среднюю амплитуду по модулю для аудиофайла."""
    try:
        data, sr = sf.read(filepath)
        data = np.asarray(data, dtype=float)

        if len(data.shape) > 1:
            data = data.mean(axis=1)

        return float(np.mean(np.abs(data)))
    except Exception:
        return 0.0


def assign_range(value: float, bin_size: float = 0.01) -> str:
    """Преобразует среднюю амплитуду в диапазон."""
    start = (value // bin_size) * bin_size
    end = start + bin_size
    return f"{start:.3f}–{end:.3f}"


def build_dataframe(csv_path: str) -> pd.DataFrame:
    """Читает CSV-аннотацию и строит датафрейм с амплитудами и диапазонами."""
    df = pd.read_csv(csv_path)
    df = df[["Относительный путь", "Абсолютный путь"]].copy()
    
    df["Средняя амплитуда"] = df["Абсолютный путь"].apply(read_audio_mean_amplitude)
    df["Диапазон амплитуды"] = df["Средняя амплитуда"].apply(assign_range)
    return df


def save_dataframe(df: pd.DataFrame, out_dir: str, filename: str) -> str:
    """Сохраняет датафрейм в файл и возвращает путь."""
    path = os.path.join(out_dir, filename)
    df.to_csv(path, index=False, encoding="utf-8")
    return path


def sort_dataframe(df: pd.DataFrame, key: str) -> pd.DataFrame:
    """Возвращает отсортированный DataFrame."""
    return df.sort_values(by=key).reset_index(drop=True)


def filter_dataframe(df: pd.DataFrame, key: str, value: str) -> pd.DataFrame:
    """Фильтрует DataFrame по значению колонки."""
    return df[df[key] == value].reset_index(drop=True)


def plot_histogram(df: pd.DataFrame, column: str, output_path: str) -> None:
    """Строит гистограмму распределения количества файлов по диапазонам амплитуды."""
    counts = df[column].value_counts().sort_index()

    plt.figure(figsize=(12, 6))
    plt.bar(counts.index, counts.values, color="steelblue")
    plt.xlabel("Диапазон средней амплитуды")
    plt.ylabel("Количество файлов")
    plt.title("Распределение файлов по средней амплитуде")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(output_path)
    plt.show()
    plt.close()
  
