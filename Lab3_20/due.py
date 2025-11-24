"""
Модуль для обработки аудиофайлов - склейка двух файлов.
"""

import os
from datetime import datetime
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np

try:
    import soundfile as sf
    SOUNDFILE_AVAILABLE = True
except ImportError:
    SOUNDFILE_AVAILABLE = False


class AudioProcessor:
    """Класс для обработки аудиофайлов с использованием NumPy."""
    
    def __init__(self, output_dir: str = "audio_results"):
        if not SOUNDFILE_AVAILABLE:
            raise ImportError("Необходима установка soundfile: pip install soundfile")
        
        self.output_dir = output_dir
        self._create_output_directory()
    
    def _create_output_directory(self):
        """Создаем папку для результатов, если она не существует."""
        abs_path = os.path.abspath(self.output_dir)
        os.makedirs(abs_path, exist_ok=True)
    
    def _get_output_path(self, filename: str) -> str:
        return os.path.join(self.output_dir, filename)
    
    def read_audio_file(self, file_path: str) -> Tuple[int, np.ndarray]:
        audio_data, sample_rate = sf.read(file_path)
        audio_data = np.asarray(audio_data)
        
        if audio_data.ndim > 1:
            audio_data = np.mean(audio_data, axis=1)
        
        if audio_data.dtype in [np.float32, np.float64]:
            audio_data = np.clip(audio_data, -1.0, 1.0)
            audio_data = (audio_data * 32767).astype(np.int16)
        
        return sample_rate, audio_data
    
    def get_audio_info(self, file_path: str) -> dict:
        sample_rate, audio_data = self.read_audio_file(file_path)
        file_size = os.path.getsize(file_path)
        
        duration = len(audio_data) / sample_rate
        
        audio_stats = {
            'min': np.min(audio_data),
            'max': np.max(audio_data),
            'mean': np.mean(audio_data),
            'rms': np.sqrt(np.mean(audio_data.astype(np.float64)**2))
        }
        
        return {
            'duration': duration,
            'sample_rate': sample_rate,
            'channels': 1,
            'samples': len(audio_data),
            'file_size_kb': file_size / 1024,
            'format': file_path.split('.')[-1].upper(),
            'stats': audio_stats
        }
    
    def resample_audio(self, audio_data: np.ndarray, original_sr: int, target_sr: int) -> np.ndarray:
        if original_sr == target_sr:
            return audio_data
        
        duration = len(audio_data) / original_sr
        target_length = int(duration * target_sr)
        
        original_time = np.linspace(0, duration, len(audio_data))
        target_time = np.linspace(0, duration, target_length)
        
        return np.interp(target_time, original_time, audio_data).astype(audio_data.dtype)
    
    def concatenate_audio(self, file1: str, file2: str, output_filename: str = None) -> str:
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"combined_audio_{timestamp}.wav"
        
        output_path = self._get_output_path(output_filename)
        
        sample_rate1, audio1 = self.read_audio_file(file1)
        sample_rate2, audio2 = self.read_audio_file(file2)
        
        if sample_rate1 != sample_rate2:
            audio2 = self.resample_audio(audio2, sample_rate2, sample_rate1)
        
        combined_audio = np.concatenate((audio1, audio2))
        sf.write(output_path, combined_audio, sample_rate1, subtype='PCM_16')
        
        return output_path
    
    def normalize_audio(self, audio_data: np.ndarray) -> np.ndarray:
        if audio_data.dtype == np.int16:
            audio_float = audio_data.astype(np.float32) / 32767.0
        else:
            audio_float = audio_data.astype(np.float32)
        
        max_val = np.max(np.abs(audio_float))
        return audio_float / max_val if max_val > 0 else audio_float
    
    def plot_audio_waveforms(self, file1: str, file2: str, output_file: str, plot_filename: str = None) -> str:
        if plot_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            plot_filename = f"audio_comparison_{timestamp}.png"
        
        plot_path = self._get_output_path(plot_filename)
        
        sample_rate1, audio1 = self.read_audio_file(file1)
        sample_rate2, audio2 = self.read_audio_file(file2)
        sample_rate_result, audio_result = self.read_audio_file(output_file)
        
        audio1_norm = self.normalize_audio(audio1)
        audio2_norm = self.normalize_audio(audio2)
        audio_result_norm = self.normalize_audio(audio_result)
        
        time1 = np.arange(len(audio1_norm)) / sample_rate1
        time2 = np.arange(len(audio2_norm)) / sample_rate2
        time_result = np.arange(len(audio_result_norm)) / sample_rate_result
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10))
        
        colors = ['#1f77b4', '#2ca02c', '#d62728']
        
        ax1.plot(time1, audio1_norm, color=colors[0], alpha=0.8, linewidth=0.8)
        ax1.set_title(f'Файл 1: {os.path.basename(file1)}', fontweight='bold')
        ax1.set_ylabel('Амплитуда')
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(time2, audio2_norm, color=colors[1], alpha=0.8, linewidth=0.8)
        ax2.set_title(f'Файл 2: {os.path.basename(file2)}', fontweight='bold')
        ax2.set_ylabel('Амплитуда')
        ax2.grid(True, alpha=0.3)
        
        ax3.plot(time_result, audio_result_norm, color=colors[2], alpha=0.8, linewidth=0.8)
        ax3.set_title(f'Результат: {os.path.basename(output_file)}', fontweight='bold')
        ax3.set_xlabel('Время (секунды)')
        ax3.set_ylabel('Амплитуда')
        ax3.grid(True, alpha=0.3)
        
        splice_time = len(audio1_norm) / sample_rate1
        ax3.axvline(x=splice_time, color='orange', linestyle='--', alpha=0.7, 
                   label=f'Склейка ({splice_time:.2f}с)')
        ax3.legend()
        
        plt.tight_layout()
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        plt.show()
        
        return plot_path
    
    def display_audio_info(self, file_path: str, title: str = "Аудиофайл"):
        info = self.get_audio_info(file_path)
        
        if info:
            print(f"\n{title}: {os.path.basename(file_path)}")
            print(f"  Длительность: {info['duration']:.2f} сек")
            print(f"  Частота: {info['sample_rate']} Hz")
            print(f"  Сэмплы: {info['samples']}")
            print(f"  Размер: {info['file_size_kb']:.1f} KB")
            print(f"  Формат: {info['format']}")
            
            stats = info['stats']
            print(f"  Амплитуда: {stats['min']:.0f} / {stats['max']:.0f} (мин/макс)")
        else:
            print(f"❌ Ошибка чтения: {file_path}")
    
    def find_audio_file(self, audio_files: List[str], filename: str) -> str:
        for file_path in audio_files:
            if os.path.basename(file_path) == filename:
                return file_path
        return ""
    
    def list_available_files(self, audio_files: List[str]):
        print("\nДОСТУПНЫЕ ФАЙЛЫ:")
        print("-" * 60)
        for i, file_path in enumerate(audio_files, 1):
            info = self.get_audio_info(file_path)
            if info:
                name = os.path.basename(file_path)
                duration = info['duration']
                size = info['file_size_kb']
                print(f"  {i:2d}. {name:30} {duration:5.1f}с {size:6.1f}KB")
            else:
                print(f"  {i:2d}. {os.path.basename(file_path):30} {'Ошибка':>10}")
        print("-" * 60)