import numpy as np
import soundfile as sf


def load_audio(filepath: str) -> tuple[np.ndarray, int]:
    """Загружает аудиофайл и возвращает данные и sample rate"""
    try:
        data, samplerate = sf.read(filepath)
        return data, samplerate
    except FileNotFoundError:
        raise


def create_echo(audio_data: np.ndarray, delay_samples: int, decay: float) -> np.ndarray:
    """Создаёт эхо-эффект путём наложения задержанного сигнала"""
    output_size = len(audio_data) + delay_samples

    if len(audio_data.shape) == 1:
        result = np.zeros(output_size, dtype=audio_data.dtype)
    else:
        result = np.zeros((output_size, audio_data.shape[1]), dtype=audio_data.dtype)

    result[: len(audio_data)] = audio_data
    result[delay_samples : delay_samples + len(audio_data)] += (audio_data * decay)

    return result


def save_audio(audio_data: np.ndarray, filepath: str, samplerate: int) -> None:
    """Сохраняет аудиофайл"""
    sf.write(filepath, audio_data, samplerate)