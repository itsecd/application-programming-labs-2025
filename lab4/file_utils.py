import numpy as np
import os
import pandas as pd
import soundfile as sf


def get_audio_path(folder: str) -> pd.DataFrame:
    """
    Сканирует директорию и формирует DataFrame.
    """

    audio_files = []
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith((".wav",
                                   ".mp3",
                                   ".ogg",
                                   ".m4a")):
                abs_path = os.path.join(root, f)
                rel_path = os.path.relpath(abs_path, folder)
                audio_files.append((abs_path, rel_path))
    return pd.DataFrame(audio_files, columns=[
        "absolute_path", "relative_path"
    ])


def calc_min_ampl(path: str) -> float | None:
    """
    Вычисляет минимальную амплитуду сигнала по модулю.
    """

    try:
        data, _ = sf.read(path)
        data = np.asarray(data, dtype=float)
        return float(np.min(np.abs(data)))
    except Exception:
        return None


def add_min_ampl_col(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавляет в DataFrame колонку "min_amplitude".
    """

    df["min_amplitude"] = df["absolute_path"].apply(calc_min_ampl)
    df = df.dropna(subset=["min_amplitude"])
    return df


def sort_by(df: pd.DataFrame) -> pd.DataFrame:
    """
    Сортирует DataFrame по минимальной амплитуде
    """

    return df.sort_values(by="min_amplitude").reset_index(drop=True)


def filter_by(df: pd.DataFrame, treshold: float) -> pd.DataFrame:
    """
    Фильтрует DataFrame по минимальной амплитуде.
    """

    return df[df["min_amplitude"] >= treshold].reset_index(drop=True)


def save_dataframe(df: pd.DataFrame, path: str) -> None:
    """
    Сохраняет DataFrame в csv файл.
    """

    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
