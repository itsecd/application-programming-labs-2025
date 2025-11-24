"""
Главный модуль для обработки аудиофайлов - склейка двух файлов.
"""

import argparse
import csv
import os
import sys
from typing import List, Tuple

from due import AudioProcessor


def load_audio_files_from_csv(csv_file: str) -> List[str]:
    audio_files = []
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        if 'absolute_path' not in reader.fieldnames:
            return []
        
        for row in reader:
            file_path = row['absolute_path']
            if os.path.exists(file_path):
                audio_files.append(file_path)
    
    return audio_files

def find_audio_files_in_directory(directory: str) -> List[str]:
    audio_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.mp3', '.wav')):
                audio_files.append(os.path.join(root, file))
    
    return audio_files


def get_user_file_selection(audio_files: List[str], processor: AudioProcessor) -> Tuple[str, str]:
    processor.list_available_files(audio_files)
    
    while True:
        try:
            print("\nВЫБОР ФАЙЛОВ")
            print("Введите два номера через пробел:")
            choice = input("Ваш выбор: ").strip()
            
            if not choice:
                continue
                
            choices = choice.split()
            if len(choices) != 2:
                print("Нужно 2 файла")
                continue
                
            idx1, idx2 = int(choices[0]) - 1, int(choices[1]) - 1
            
            if 0 <= idx1 < len(audio_files) and 0 <= idx2 < len(audio_files):
                file1, file2 = audio_files[idx1], audio_files[idx2]
                
                if file1 == file2:
                    print("Выберите разные файлы")
                    continue
                    
                return file1, file2
            else:
                print(f"Номера от 1 до {len(audio_files)}")
                
        except ValueError:
            print("Введите числа")


def main():
    """Главная функция программы."""
    parser = argparse.ArgumentParser(description='Склейка двух аудиофайлов')
    
    parser.add_argument('--csv_annotation', help='CSV файл с путями')
    parser.add_argument('--audio_dir', help='Папка с аудиофайлами')
    parser.add_argument('--output', default='audio_results', help='Папка для результатов')
    parser.add_argument('--file1', help='Первый файл')
    parser.add_argument('--file2', help='Второй файл')
    
    args = parser.parse_args()
    
    if not args.csv_annotation and not args.audio_dir:
        print("Укажите --csv_annotation или --audio_dir")
        sys.exit(1)
    
    print("=== СКЛЕЙКА АУДИО ===")
    
    audio_files = []
    
    if args.csv_annotation and os.path.exists(args.csv_annotation):
        audio_files = load_audio_files_from_csv(args.csv_annotation)
        print(f"Загружено файлов из CSV: {len(audio_files)}")
    elif args.audio_dir and os.path.exists(args.audio_dir):
        audio_files = find_audio_files_in_directory(args.audio_dir)
        print(f"Найдено файлов в папке: {len(audio_files)}")
    
    if len(audio_files) < 2:
        print("Нужно минимум 2 файла")
        sys.exit(1)
    
    try:
        processor = AudioProcessor(output_dir=args.output)
    except ImportError as e:
        print(f" {e}")
        sys.exit(1)
    
    try:
        file1, file2 = None, None
        
        if args.file1 and args.file2:
            file1 = processor.find_audio_file(audio_files, args.file1)
            file2 = processor.find_audio_file(audio_files, args.file2)
        
        if not file1 or not file2:
            file1, file2 = get_user_file_selection(audio_files, processor)
        
        print(f"\nВыбрано:")
        print(f"  1. {os.path.basename(file1)}")
        print(f"  2. {os.path.basename(file2)}")
        
        processor.display_audio_info(file1, "Файл 1")
        processor.display_audio_info(file2, "Файл 2")
        
        print(f"\nСклейка...")
        result_path = processor.concatenate_audio(file1, file2)
        
        if result_path:
            print(f"Успешно: {result_path}")
            
            print(f"\nГрафики...")
            plot_path = processor.plot_audio_waveforms(file1, file2, result_path)
            
            if plot_path:
                print(f"\nГотово!")
                print(f"Папка: {os.path.abspath(args.output)}")
                print(f"  Аудио: {os.path.basename(result_path)}")
                print(f"  График: {os.path.basename(plot_path)}")
            
        else:
            print("Ошибка склейки")
            sys.exit(1)
            
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()