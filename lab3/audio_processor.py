import os

import numpy as np
import soundfile as sf
from typing import Tuple, Optional

def read_audio_file(file_path: str) -> Tuple[np.ndarray, int, int]:
    """Чтение аудиофайла"""

    try:
        audio_data, sample_rate = sf.read(file_path)

        if len(audio_data.shape) == 1:
            channels = 1
            print(f"Аудио: моно, {len(audio_data)} семплов")
        else:
            channels = audio_data.shape[1]
            print(f"Аудио: стерео ({channels} канала), {len(audio_data)} семплов")

        print(f"Частота дискретизации: {sample_rate} Гц")
        print(f"Длительность: {len(audio_data) / sample_rate:.2f} секунд")
        print(f"Тип данных: {audio_data.dtype}")

        return audio_data, sample_rate, channels
    
    except Exception as e:
        raise Exception (f"Ошибка при чтении файла: {e}, \n Проверьте, что файл является поддерживаемым аудиоформатом (WAV, FLAC и др.)")


def reverse_audio(audio_data: np.ndarray) -> np.ndarray:
    """Переворачивает аудио задом наперед"""
    return np.flip(audio_data, axis=0)


def save_audio_file(
    audio_data: np.ndarray, 
    sample_rate: int, 
    output_path: str
) -> None:
    """Сохранение аудиофайла"""
    try:
        sf.write(output_path, audio_data, sample_rate)
        print(f"Файл успешно сохранен: {output_path}")
        print(f"Размер файла: {os.path.getsize(output_path) / 1024:.2f} KB")
    except Exception as e:
        raise Exception(f"Ошибка при сохранении файла: {e}")
