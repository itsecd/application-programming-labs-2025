import soundfile as sf
import numpy as np


def file_info(path: str) -> tuple[int, float]:
    """
    Возвращает (количество сэмплов, длительность в секундах).
    """
    data, samplerate = sf.read(path)
    num_samples = len(data)
    duration = num_samples / samplerate
    return num_samples, duration


def remove_silence(data: np.ndarray, threshold: float) -> np.ndarray:
    """
    Удаляет участки, где |амплитуда| < threshold.
    """
    if data.ndim == 1:
        mask = np.abs(data) >= threshold
        return data[mask]

    amp = np.max(np.abs(data), axis=1)
    mask = amp >= threshold
    return data[mask, :]
