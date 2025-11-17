import os
import numpy as np
import soundfile as sf

def load_audio(path: str) -> tuple:
    """
    Загружает аудиофайл и возвращает данные и частоту дискретизации.
    """
    data, samplerate = sf.read(path)
    return data, samplerate


def get_duration(data: np.ndarray,
                 samplerate: int) -> float:
    """
    Возвращает длительность аудио в секундах
    """
    return len(data) / samplerate


def validate_range(start_sec: float,
                   end_sec: float,
                   duration: float) -> bool:
    """
    Проверяет корректность диапазона обрезки аудиофайла
    """
    return 0 <= start_sec < end_sec <= duration


def trim_audio(data: np.ndarray,
               samplerate: int,
               start_sec: float,
               end_sec: float) -> np.ndarray:
    """
    Обрезает аудиофайл в заданном диапазоне
    """
    start_sample = int(start_sec * samplerate)
    end_sample = int(end_sec * samplerate)
    return data[start_sample:end_sample]


def save_audio(data: np.ndarray,
               samplerate: int,
               output_path: str) -> None:
    """
    Сохраняет аудиофайл по указанному пути
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sf.write(output_path, data, samplerate)
