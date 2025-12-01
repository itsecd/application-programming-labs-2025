"""Модуль для обработки аудиофайлов и извлечения метаданных."""
import os
from typing import Any, Dict

import librosa


class AudioProcessor:
    """Класс для обработки аудиофайлов и извлечения метаданных."""

    @staticmethod
    def get_audio_duration(file_path: str) -> float:
        """
        Получает длительность аудиофайла в секундах.

        Args:
            file_path: Путь к аудиофайлу

        Returns:
            Длительность аудиофайла в секундах

        Raises:
            Exception: Если произошла ошибка при обработке файла
        """
        try:
            duration = librosa.get_duration(path=file_path)
            return round(duration, 2)
        except Exception as e:
            raise Exception(f"Ошибка при получении длительности файла {file_path}: {e}")