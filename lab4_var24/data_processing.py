import numpy as np
import pandas as pd
import soundfile as sf



def create_df(path_csv: str) -> pd.DataFrame:
    """
    Формируем датафрейм из csv файла
    """
    return pd.read_csv(path_csv, usecols=[1, 2])


def get_amplitude(path_audio: str) -> float:
    """
    Получение средней амплитуды
    """
    data, sr = sf.read(path_audio)
    mean_amp = np.mean(np.abs(data))
    return mean_amp


def add_amplitude(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавление новой колонки с амплитудой
    """
    amplitudes = []
    for idx, row in df.iterrows():
        amplitude = get_amplitude(row['abs_path'])
        amplitudes.append(amplitude)
    df['amplitude'] = amplitudes
    return df    


def sort_by_amplitude(df: pd.DataFrame) -> pd.DataFrame:
    """
    Сортирует датафрейм по амплитуде 
    """
    df = df.sort_values('amplitude').reset_index(drop=True)
    return df


def filtr_amplitude(df: pd.DataFrame, min_ampl: float = None, max_ampl: float = None) -> pd.DataFrame:
    """
    Фильтрует датафрейм по амплитуде 
    """
    filtered_df = df.copy()
    
    filtered_df = filtered_df[filtered_df['amplitude'] >= min_ampl]
    
    filtered_df = filtered_df[filtered_df['amplitude'] <= max_ampl]
    
    return filtered_df
