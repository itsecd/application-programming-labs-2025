"""
Модуль для обработки аудиофайлов - уменьшение скорости.
Вариант 26: Уменьшите скорость аудиофайла в заданное количество раз.
"""

import numpy as np
import soundfile as sf
import argparse
from pathlib import Path
import matplotlib.pyplot as plt


class AudioSpeedReducer:
    """Класс для уменьшения скорости аудиофайлов."""
    
    def __init__(self):
        self.original_audio = None
        self.sample_rate = None
    
    def load_audio(self, file_path: str):
        """Загружает аудиофайл."""
        try:
            data, sample_rate = sf.read(file_path)
            self.original_audio = data
            self.sample_rate = sample_rate
            return data, sample_rate
        except Exception as e:
            raise Exception(f"Ошибка загрузки аудио: {e}")
    
    def reduce_speed(self, slowdown_factor: float):
        """Уменьшает скорость аудио в заданное количество раз."""
        if self.original_audio is None:
            raise ValueError("Аудио не загружено")
        
        # Для ЗАМЕДЛЕНИЯ нужно УВЕЛИЧИТЬ длину
        original = self.original_audio
        new_length = int(len(original) * slowdown_factor)  # ИЗМЕНИЛИ ЗДЕСЬ!
        
        if len(original.shape) == 1:
            # Моно аудио
            time_original = np.arange(len(original))
            time_new = np.linspace(0, len(original)-1, new_length)
            processed_audio = np.interp(time_new, time_original, original)
        else:
            # Стерео аудио
            processed_audio = np.zeros((new_length, original.shape[1]))
            for channel in range(original.shape[1]):
                time_original = np.arange(len(original))
                time_new = np.linspace(0, len(original)-1, new_length)
                processed_audio[:, channel] = np.interp(
                    time_new, time_original, original[:, channel]
                )
        
        return processed_audio
    
    def save_audio(self, file_path: str, audio_data: np.ndarray):
        """Сохраняет обработанное аудио."""
        try:
            sf.write(file_path, audio_data, self.sample_rate)
        except Exception as e:
            raise Exception(f"Ошибка сохранения аудио: {e}")


def main():
    """Главная функция обработки аудио."""
    parser = argparse.ArgumentParser(
        description='Уменьшение скорости аудиофайла в заданное количество раз'
    )
    
    parser.add_argument('--input', required=True, help='Путь к исходному аудиофайлу')
    parser.add_argument('--output', required=True, help='Путь для сохранения обработанного аудио')
    parser.add_argument('--slowdown', type=float, required=True, help='Коэффициент замедления')
    
    args = parser.parse_args()
    
    try:
        # Обработка аудио
        processor = AudioSpeedReducer()
        audio_data, sample_rate = processor.load_audio(args.input)
        
        original_duration = len(audio_data) / sample_rate
        print(f"Загружено аудио: {len(audio_data)} сэмплов, {sample_rate} Гц")
        print(f"Длительность: {original_duration:.2f} сек")
        
        processed_audio = processor.reduce_speed(args.slowdown)
        processor.save_audio(args.output, processed_audio)
        
        new_duration = len(processed_audio) / sample_rate
        print(f"Сохранено замедленное аудио: {len(processed_audio)} сэмплов")
        print(f"Новая длительность: {new_duration:.2f} сек")
        print(f"Замедление в {new_duration/original_duration:.2f} раз")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    main()