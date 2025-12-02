import numpy as np
import matplotlib.pyplot as plt
import os

class AudioVisualizer:
    """Класс для визуализации аудиоданных"""
    
    def create_comparison_plot(self, original1, original2, mixed, samplerate, output_path)-> None:
        """Визуализация исходных аудио и результата смешения"""
        time1 = np.arange(len(original1)) / samplerate
        time2 = np.arange(len(original2)) / samplerate  
        time_mixed = np.arange(len(mixed)) / samplerate
        
        plt.figure(figsize=(15, 10))
        
        plt.subplot(3, 1, 1)
        self._plot_audio_channel(time1, original1, 'blue', 'Исходный аудиофайл 1')
        
        plt.subplot(3, 1, 2)
        self._plot_audio_channel(time2, original2, 'green', 'Исходный аудиофайл 2')
        
        plt.subplot(3, 1, 3)
        self._plot_audio_channel(time_mixed, mixed, 'purple', 'Смешанный аудиофайл')
        
        plt.tight_layout()
        
        plot_path = os.path.splitext(output_path)[0] + '_plot.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"График сохранен как: {plot_path}")
        
        plt.show()

    def _plot_audio_channel(self, time, audio, color, title)-> None:
        """Вспомогательный метод для построения графика аудиоканала"""
        if len(audio.shape) == 1:
            plt.plot(time, audio, color=color, alpha=0.7)
        else:
            plt.plot(time, audio[:, 0], color='blue', alpha=0.7, label='Левый канал')
            plt.plot(time, audio[:, 1], color='red', alpha=0.7, label='Правый канал')
            plt.legend()
        
        plt.title(title)
        plt.xlabel('Время (секунды)')
        plt.ylabel('Амплитуда')
        plt.grid(True, alpha=0.3)