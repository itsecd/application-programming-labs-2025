import numpy
import argparse
import soundfile as sf
import matplotlib.pyplot as plt
import os





def load_music(path:str) ->  np.ndarray:
    data, samplerate = sf.read(filepath)
    return data

def create_echo(audio_data: np.ndarray, delay_samples: int, decay: float) -> np.ndarray:
    output_size = len(audio_data) + delay_samples
    result = np.zeros(output_size, dtype=audio_data.dtype)
    
    result[:len(audio_data)] = audio_data
    
    result[delay_samples:delay_samples + len(audio_data)] += audio_data * decay
    
    return result

def save_audio(audio_data: np.ndarray, filepath: str, samplerate: int = 44100) -> None:
     sf.write(filepath, audio_data, samplerate)
     
def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.
    
    Returns:
        argparse.Namespace: объект с аргументами
    """
    
    parser = argparse.ArgumentParser(
        description='Применяет эхо-эффект к аудиофайлу'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='Путь к исходному аудиофайлу'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Путь для сохранения результата'
    )
   
    
    return parser.parse_args()