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
    
    def process_audio(self, input_path, output_path, auto_play=False):
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
            
            if auto_play:
                self.play_audio(output_path)
            
            return True
            
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
    
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
    
    args = parser.parse_args()
    
    processor = AudioReverser()
    
    if not processor.check_dependencies():
        return
    
    if processor.process_audio(args.input, args.output, args.play):
        print("Готово")
    else:
        print("Ошибка")

if __name__ == "__main__":
    main()