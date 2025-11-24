#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import numpy as np
import sys
from audio_processor import AudioProcessor
from pathlib import Path


def parse_arguments() -> argparse.Namespace:
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description='Обработка аудиофайлов: изменение амплитуды'
    )
    
    parser.add_argument(
        'input_file',
        type=str,
        help='Путь к входному аудиофайлу'
    )
    
    parser.add_argument(
        'output_file', 
        type=str,
        help='Путь для сохранения обработанного аудиофайла'
    )
    
    parser.add_argument(
        '--amplitude_factor',
        type=float,
        required=True,
        help='Коэффициент увеличения амплитуды'
    )
    
    return parser.parse_args()


def validate_paths(input_path: str, output_path: str) -> bool:
    """Проверяет корректность путей к файлам."""
    input_file = Path(input_path)
    
    if not input_file.exists():
        print(f"Ошибка: входной файл не найден: {input_path}")
        return False
    
    if not input_file.is_file():
        print(f"Ошибка: указанный путь не является файлом: {input_path}")
        return False
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    return True


def plot_audio_comparison(original_audio: np.ndarray, 
                         processed_audio: np.ndarray, 
                         sample_rate: int,
                         amplitude_factor: float) -> None:
    """
    Создает графики для сравнения исходного и обработанного аудио.
    
    Args:
        original_audio: Исходные аудиоданные
        processed_audio: Обработанные аудиоданные  
        sample_rate: Частота дискретизации
        amplitude_factor: Коэффициент увеличения амплитуды
    """
    duration = len(original_audio) / sample_rate
    time_axis = np.linspace(0, duration, len(original_audio))
    
    plt.figure(figsize=(12, 8))
    
    #Исходное аудио
    plt.subplot(2, 1, 1)
    if len(original_audio.shape) > 1:  
        plt.plot(time_axis, original_audio[:, 0], label='Левый канал', alpha=0.8, linewidth=0.8)
        plt.plot(time_axis, original_audio[:, 1], label='Правый канал', alpha=0.8, linewidth=0.8)
    else:  
        plt.plot(time_axis, original_audio, label='Аудиосигнал', color='blue', linewidth=0.8)
    
    plt.title('Исходное аудио')
    plt.xlabel('Время (с)')
    plt.ylabel('Амплитуда')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(-1, 1)
    
    #Обработанное аудио
    plt.subplot(2, 1, 2)
    if len(processed_audio.shape) > 1:  
        plt.plot(time_axis, processed_audio[:, 0], label='Левый канал', alpha=0.8, linewidth=0.8)
        plt.plot(time_axis, processed_audio[:, 1], label='Правый канал', alpha=0.8, linewidth=0.8)
    else: 
        plt.plot(time_axis, processed_audio, label='Аудиосигнал', color='red', linewidth=0.8)
    
    plt.title(f'Обработанное аудио (увеличение амплитуды в {amplitude_factor} раз)')
    plt.xlabel('Время (с)')
    plt.ylabel('Амплитуда')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(-1, 1)
    
    plt.tight_layout()
    plt.show()


def main() -> None:
    """Основная функция программы."""
    try:
        args = parse_arguments()
        
        if not validate_paths(args.input_file, args.output_file):
            sys.exit(1)
        
        if args.amplitude_factor <= 0:
            print("Ошибка: коэффициент амплитуды должен быть положительным числом")
            sys.exit(1)
        
        print("Обработка аудиофайла...")
        print(f"Входной файл: {args.input_file}")
        print(f"Выходной файл: {args.output_file}")
        print(f"Коэффициент амплитуды: {args.amplitude_factor}")
        print()
        
       
        processor = AudioProcessor()
        
        
        print("Загрузка аудиофайла...")
        audio_data, sample_rate = processor.load_audio(args.input_file)
        
        
        print("Информация о аудио:")
        print(f"  Размер аудиоданных: {audio_data.shape}")
        print(f"  Частота дискретизации: {sample_rate} Hz")
        print(f"  Длительность: {len(audio_data) / sample_rate:.2f} секунд")
        
        if len(audio_data.shape) > 1:
            print(f"  Количество каналов: {audio_data.shape[1]}")
            print(f"  Количество сэмплов: {audio_data.shape[0]}")
        else:
            print(f"  Количество каналов: 1 (моно)")
            print(f"  Количество сэмплов: {audio_data.shape[0]}")
        print()
        
        
        print("Увеличение амплитуды...")
        amplified_audio = processor.amplify_audio(audio_data, args.amplitude_factor)
        
        
        print("Создание графиков...")
        plot_audio_comparison(audio_data, amplified_audio, sample_rate, args.amplitude_factor)
        
       
        print("Сохранение результата...")
        processor.save_audio(args.output_file, amplified_audio, sample_rate)
        
        print("Обработка завершена успешно!")
        
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()