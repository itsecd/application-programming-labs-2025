import sys
import os

# Импортируем модули
from arg_parser import (parse_arguments)
from audio_processor import read_audio_file, reverse_audio, save_audio_file
from visualizer import plot_audio_comparison

def main():
    """Основная функция"""

    args = parse_arguments()
    
    print("=" * 50)
    print("Чтение аудиофайла...")
    audio_data, sample_rate, channels = read_audio_file(args.input_file)
    
    print("\n" + "=" * 50)
    print("Переворачивание аудио задом наперед...")
    reversed_audio = reverse_audio(audio_data)
    
    print("\n" + "=" * 50)
    print("Визуализация результатов...")
    plot_audio_comparison(audio_data, reversed_audio, sample_rate, 
                          args.input_file, args.output_file)
    
    print("\n" + "=" * 50)
    print("Сохранение результата...")
    save_audio_file(reversed_audio, sample_rate, args.output_file)
    
    print("\n" + "=" * 50)
    print("Готово!")
    print(f"Оригинальный файл: {args.input_file}")
    print(f"Обработанный файл: {args.output_file}")

if __name__ == "__main__":
    main()