import numpy as np
import pandas as pd
import soundfile as sf


def add_amplitude_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавляет столбик range_amplitude для каждого файла
    """
    df["range_amplitude"] = 0.0

    for i, path in enumerate(df["absolute_path"]):
        try:
            data, samplerate = sf.read(path)
            range_ampl = np.max(data) - np.min(data)
            df.loc[i, "range_amplitude"] = range_ampl
        except Exception as e:
            print(f"Ошибка при чтении {path}: {e}")

    return df


def filter_by_amplitude(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """
    Фильтрует DataFrame по range_amplitude > threshold
    """
    filtered_df = df[df["range_amplitude"] > threshold].reset_index(drop=True)
    filtered_df.index += 1
    return filtered_df


def sort_by_amplitude(df: pd.DataFrame, ascending: bool = True) -> pd.DataFrame:
    """
    Сортирует DataFrame по range_amplitude
    """
    sorted_df = df.sort_values("range_amplitude", ascending=ascending).reset_index(
        drop=True
    )
    sorted_df.index += 1
    return sorted_df
