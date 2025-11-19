import pandas as pd 
import soundfile as sf
import matplotlib.pyplot as plt

def create_df(path_csv):
    """
    Формируем датафрейм из csv файла
    """
    return pd.read_csv(path_csv, usecols=[1, 2])



def get_amplitude(path_audio):
    """
    Получение средней амплитуды
    """
    data,  = sf.read(path_audio)
    mean_amp = np.mean(np.abs(data))
    return mean_amp



def add_amplitude(df):
    amplitudes = []
    for idx, row in df.iterrows():
        amplitude = get_amplitude(row['absolute_path'])
        amplitudes.append(amplitude)
    df['amplitude'] = amplitudes
    return df    
        
