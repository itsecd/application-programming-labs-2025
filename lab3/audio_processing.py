import numpy as np
import soundfile as sf
from typing import Tuple

def read_audio_file(file_path: str) -> Tuple[np.ndarray, int]:
    """Читает аудиофайл mp3 или wav."""
    audio_data, sample_rate = sf.read(file_path)
    return audio_data, sample_rate

def stereo_to_mono(audio_data: np.ndarray) -> np.ndarray:
    """Приводит стерео аудио к моно."""
    if audio_data.ndim == 1:
        return audio_data
    return audio_data.mean(axis=1)

def limit_amplitude(audio_data: np.ndarray, threshold: float) -> np.ndarray:
    """Ограничивает амплитуду выше порога threshold."""
    limited_audio = np.copy(audio_data)
    limited_audio[limited_audio > threshold] = threshold
    limited_audio[limited_audio < -threshold] = -threshold
    return limited_audio

def save_audio(file_path: str, audio_data: np.ndarray, sample_rate: int) -> None:
    """Сохраняет аудио в mp3 или wav, создавая директории."""
    import os
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    sf.write(file_path, audio_data, sample_rate)
