import numpy as np
import soundfile as sf

def transformations(source: str, music: str, alpha: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Функция увеличивает музыку в alpha раз
    """
    data, samplerate = sf.read(source)
    data_sped = data[::alpha]
    
    t_orig = np.arange(len(data)) / samplerate
    t_sped = np.arange(len(data_sped)) / samplerate
    
    sf.write(music, data_sped, samplerate, format="WAV")
    
    return data, data_sped, t_orig, t_sped
