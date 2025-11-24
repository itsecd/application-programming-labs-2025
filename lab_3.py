import argparse
from pathlib import Path
import numpy as np
import sys
import os

try:
    import soundfile as sf
    SOUNDFILE_AVAILABLE = True
except ImportError:
    SOUNDFILE_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

class AudioReverser:
    def __init__(self):
        self.supported_formats = {'.wav', '.flac', '.ogg'}
        if SOUNDFILE_AVAILABLE:
            try:
                self.supported_formats.add('.mp3')
            except:
                pass
    
    def check_dependencies(self):
        if not SOUNDFILE_AVAILABLE:
            print("Установите: pip install soundfile")
            return False
        return True
    
    def process_audio(self, input_path, output_path, auto_play=False, show_plot=False):
        input_path = Path(input_path)
        
        if not input_path.exists():
            print(f"Файл не найден: {input_path}")
            return False
        
        if input_path.suffix.lower() not in self.supported_formats:
            print(f"Формат не поддерживается: {input_path.suffix}")
            return False
        
        print(f"Обработка: {input_path.name}")
        
        try:
            # Загружаем аудио
            audio_data, sample_rate = sf.read(input_path)
            
            # Переворачиваем
            reversed_audio = np.flip(audio_data, axis=0)
            
            # Сохраняем
            sf.write(output_path, reversed_audio, sample_rate)
            
            print(f"Сохранен: {Path(output_path).name}")
            
            if show_plot and MATPLOTLIB_AVAILABLE:
                self.visualize_audio(audio_data, reversed_audio, sample_rate, 
                                   Path(input_path).name, Path(output_path).name)
            
            if auto_play:
                self.play_audio(output_path)
            
            return True
            
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
    
    def visualize_audio(self, original_audio, reversed_audio, sample_rate, 
                       original_name, reversed_name):
        """Визуализирует исходный и перевернутый аудиосигналы"""
        try:
            # Создаем временные оси
            duration_original = len(original_audio) / sample_rate
            time_original = np.linspace(0, duration_original, len(original_audio))
            
            duration_reversed = len(reversed_audio) / sample_rate
            time_reversed = np.linspace(0, duration_reversed, len(reversed_audio))
            
            # Создаем график
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
            
            # Отображаем исходный аудиосигнал
            if original_audio.ndim == 1:  # Моно
                ax1.plot(time_original, original_audio, color='blue', linewidth=0.5)
                ax1.set_ylabel('Амплитуда')
            else:  # Стерео
                ax1.plot(time_original, original_audio[:, 0], color='blue', 
                        linewidth=0.5, alpha=0.7, label='Левый канал')
                ax1.plot(time_original, original_audio[:, 1], color='red', 
                        linewidth=0.5, alpha=0.7, label='Правый канал')
                ax1.legend()
            
            ax1.set_title(f'Исходный аудио: {original_name}')
            ax1.set_xlabel('Время (сек)')
            ax1.grid(True, alpha=0.3)
            
            # Отображаем перевернутый аудиосигнал
            if reversed_audio.ndim == 1:  # Моно
                ax2.plot(time_reversed, reversed_audio, color='green', linewidth=0.5)
                ax2.set_ylabel('Амплитуда')
            else:  # Стерео
                ax2.plot(time_reversed, reversed_audio[:, 0], color='green', 
                        linewidth=0.5, alpha=0.7, label='Левый канал')
                ax2.plot(time_reversed, reversed_audio[:, 1], color='orange', 
                        linewidth=0.5, alpha=0.7, label='Правый канал')
                ax2.legend()
            
            ax2.set_title(f'Перевернутый аудио: {reversed_name}')
            ax2.set_xlabel('Время (сек)')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"Ошибка при визуализации: {e}")
    
    def play_audio(self, file_path):
        try:
            file_path = Path(file_path)
            if sys.platform == "win32":
                os.startfile(file_path)
            elif sys.platform == "darwin":
                import subprocess
                subprocess.run(["afplay", str(file_path)], check=False)
            else:
                import subprocess
                subprocess.run(["aplay", str(file_path)], check=False)
        except:
            pass

def main():
    parser = argparse.ArgumentParser(description='Перевернуть аудио')
    parser.add_argument('--input', '-i', required=True, help='Входной файл')
    parser.add_argument('--output', '-o', required=True, help='Выходной файл')
    parser.add_argument('--play', '-p', action='store_true', help='Проиграть результат')
    parser.add_argument('--plot', action='store_true', help='Показать графики аудио')
    
    args = parser.parse_args()
    
    processor = AudioReverser()
    
    if not processor.check_dependencies():
        return
    
    if args.plot and not MATPLOTLIB_AVAILABLE:
        print("Для визуализации установите: pip install matplotlib")
        args.plot = False
    
    if processor.process_audio(args.input, args.output, args.play, args.plot):
        print("Готово")
    else:
        print("Ошибка")

if __name__ == "__main__":
    main()