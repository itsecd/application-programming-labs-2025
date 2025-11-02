import numpy
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

