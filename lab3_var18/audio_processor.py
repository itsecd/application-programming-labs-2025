"""
Модуль для работы с аудиофайлами.
"""

import numpy as np
from typing import Tuple
import librosa
import soundfile as sf


class AudioProcessor:
    """Класс для обработки аудиофайлов."""
    
    def load_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        Считывает аудио из файла.
        
        Args:
            file_path: Путь к аудиофайлу
            
        Returns:
            Tuple[np.ndarray, int]: (аудиоданные, частота дискретизации)
        """
        try:
            # Загружаем аудио, сохраняя оригинальные каналы
            audio_data, sample_rate = librosa.load(file_path, sr=None, mono=False)
            
            # Если аудио стерео, преобразуем к форме (samples, channels)
            if len(audio_data.shape) > 1:
                audio_data = audio_data.T  # Транспонируем: (channels, samples) -> (samples, channels)
            
            return audio_data, sample_rate
        except Exception as e:
            raise Exception(f"Ошибка при загрузке аудиофайла: {str(e)}")
    
    def amplify_audio(self, audio_data: np.ndarray, factor: float) -> np.ndarray:
        """
        Увеличивает амплитуду сэмплов аудиофайла.
        
        Args:
            audio_data: Исходные аудиоданные
            factor: Коэффициент увеличения амплитуды
            
        Returns:
            np.ndarray: Аудиоданные с увеличенной амплитудой
        """
        if factor <= 0:
            raise ValueError("Коэффициент амплитуды должен быть положительным")
        
        # Увеличиваем амплитуду ВСЕХ каналов
        amplified_audio = audio_data * factor
        amplified_audio = np.clip(amplified_audio, -1.0, 1.0)
        
        return amplified_audio
    
    def save_audio(self, file_path: str, audio_data: np.ndarray, sample_rate: int) -> None:
        """
        Сохраняет аудиоданные в файл.
        
        Args:
            file_path: Путь для сохранения
            audio_data: Аудиоданные для сохранения
            sample_rate: Частота дискретизации
        """
        try:
            sf.write(file_path, audio_data, sample_rate)
        except Exception as e:
            raise Exception(f"Ошибка при сохранении аудиофайла: {str(e)}")