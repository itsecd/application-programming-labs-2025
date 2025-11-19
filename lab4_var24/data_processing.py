import pandas as pd
import soundfile as sf
import numpy as np


def create_df(path_csv):
    """
    Формируем датафрейм из csv файла
    """
    return pd.read_csv(path_csv, usecols=[1, 2])


def get_amplitude(path_audio):
    """
    Получение средней амплитуды
    """
    data, sr = sf.read(path_audio)
    mean_amp = np.mean(np.abs(data))
    return mean_amp


def add_amplitude(df):
    amplitudes = []
    for idx, row in df.iterrows():
        amplitude = get_amplitude(row['abs_path'])
        amplitudes.append(amplitude)
    df['amplitude'] = amplitudes
    return df    


def sort_by_amplitude(df):
    """
    Сортирует датафрейм по амплитуде (от меньшей к большей)
    """
    df = df.sort_values('amplitude', na_position='last').reset_index(drop=True)
    return df


def filtr_amplitude(df, min_ampl, max_ampl):
    filtered_df = df.copy()
    
    filtered_df = filtered_df[filtered_df['amplitude'] >= min_ampl]
    
    filtered_df = filtered_df[filtered_df['amplitude'] <= max_ampl]
    
    return filtered_df
