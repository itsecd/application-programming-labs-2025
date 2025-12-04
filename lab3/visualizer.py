import numpy as np
import matplotlib.pyplot as plt
import os

def plot_audio_comparison(original, reversed_audio, sample_rate, original_file, output_file):
    """Визуализация оригинального и перевернутого аудио"""
    # Создаем временную шкалу
    time_original = np.arange(len(original)) / sample_rate
    time_reversed = np.arange(len(reversed_audio)) / sample_rate
    
    # Создаем фигуру с несколькими субплогами
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    
    # График оригинального аудио
    if len(original.shape) == 1:  # Моно
        axes[0].plot(time_original, original, color='blue', alpha=0.7)
        axes[0].set_title(f'Оригинальное аудио: {os.path.basename(original_file)}')
    else:  # Стерео
        axes[0].plot(time_original, original[:, 0], color='blue', alpha=0.7, label='Левый канал')
        axes[0].plot(time_original, original[:, 1], color='red', alpha=0.7, label='Правый канал')
        axes[0].legend()
        axes[0].set_title(f'Оригинальное аудио (стерео): {os.path.basename(original_file)}')
    
    axes[0].set_xlabel('Время (сек)')
    axes[0].set_ylabel('Амплитуда')
    axes[0].grid(True, alpha=0.3)
    
    # График перевернутого аудио
    if len(reversed_audio.shape) == 1:  # Моно
        axes[1].plot(time_reversed, reversed_audio, color='green', alpha=0.7)
        axes[1].set_title('Перевернутое аудио (задом наперед)')
    else:  # Стерео
        axes[1].plot(time_reversed, reversed_audio[:, 0], color='blue', alpha=0.7, label='Левый канал')
        axes[1].plot(time_reversed, reversed_audio[:, 1], color='red', alpha=0.7, label='Правый канал')
        axes[1].legend()
        axes[1].set_title('Перевернутое аудио (задом наперед)')
    
    axes[1].set_xlabel('Время (сек)')
    axes[1].set_ylabel('Амплитуда')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()