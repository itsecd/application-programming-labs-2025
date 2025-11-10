"""
Главный модуль программы для скачивания аудиофайлов с созданием аннотации.
"""

import argparse
import csv
import os
import sys
from typing import List

from audio_downloader import AudioDownloader
from file_iterator import AudioIterator


class AudioManager:
    """Менеджер для управления процессом скачивания аудиофайлов и создания аннотации."""
    
    def __init__(self, download_dir: str, annotation_file: str):
        """Инициализация менеджера с указанием директории и файла аннотации."""
        self.download_dir = download_dir
        self.annotation_file = annotation_file
        self.downloader = AudioDownloader(download_dir)

    def download_audio_collection(self, total_count: int) -> int:
        """Скачивает коллекцию аудиофайлов для всех инструментов."""
        instruments = ['trumpet', 'ukulele', 'harp']
        distribution = self._distribute_counts(total_count, instruments)
        
        print("Начинаем скачивание аудиофайлов...")
        print(f"Общее количество файлов: {total_count}")
        total_downloaded = 0
        
        for instrument, count in distribution.items():
            print(f"Инструмент: {instrument}, запланировано файлов: {count}")
            downloaded = self.downloader.download_instrument_audio(instrument, count)
            total_downloaded += downloaded
            print(f"Успешно скачано: {downloaded}/{count}")

        return total_downloaded

    def _distribute_counts(self, total_count: int, instruments: List[str]) -> dict:
        """Распределяет общее количество файлов между инструментами поровну."""
        count_per_instrument = total_count // len(instruments)
        remainder = total_count % len(instruments)
        
        distribution = {}
        for i, instrument in enumerate(instruments):
            # Распределяем остаток по первым инструментам
            distribution[instrument] = count_per_instrument + (1 if i < remainder else 0)
        
        print("Распределение файлов по инструментам:")
        for instrument, count in distribution.items():
            print(f"  {instrument}: {count} файлов")
        
        return distribution

    def create_annotation(self) -> bool:
        """Создает CSV файл аннотации с путями к скачанным файлам."""
        try:
            files_info = self.downloader.get_downloaded_files_info()
            
            if not files_info:
                print("Нет файлов для создания аннотации")
                return False
            
            with open(self.annotation_file, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["filename", "absolute_path", "relative_path"])
                
                for file_info in sorted(files_info, key=lambda x: x['filename']):
                    writer.writerow([
                        file_info['filename'],
                        file_info['absolute_path'],
                        file_info['relative_path']
                    ])
            
            print(f"Аннотация создана: {self.annotation_file}")
            print(f"Записано файлов: {len(files_info)}")
            return True
            
        except Exception as e:
            print(f"Ошибка создания аннотации: {e}")
            return False

    def demonstrate_iterator(self) -> None:
        """Демонстрирует работу итератора с файлами аннотации."""
        try:
            print("Демонстрация работы итератора:")
            
            iterator = AudioIterator(self.annotation_file)
            
            file_count = 0
            print("Первые 5 файлов в аннотации:")
            
            for filepath in iterator:
                if file_count < 5:
                    filename = os.path.basename(filepath)
                    print(f"  {file_count + 1}. {filename}")
                file_count += 1
            
            if file_count > 5:
                print(f"  ... и еще {file_count - 5} файлов")
            
            print(f"Всего файлов в итераторе: {file_count}")
            
        except Exception as e:
            print(f"Ошибка демонстрации итератора: {e}")


def parse_arguments():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description='Скачивание аудиофайлов для trumpet, ukulele и harp с созданием аннотации'
    )
    
    parser.add_argument('--output_dir', required=True, help='Путь к папке для сохранения аудиофайлов')
    parser.add_argument('--csv_path', required=True, help='Путь к файлу для CSV аннотации')
    parser.add_argument('--count', type=int, default=60, choices=range(50, 1001), 
                       help='Общее количество файлов для скачивания (50-1000)')
    
    return parser.parse_args()


def validate_arguments(args) -> bool:
    """Проверяет корректность аргументов командной строки."""
    if not (50 <= args.count <= 1000):
        print("Ошибка: количество файлов должно быть от 50 до 1000")
        return False
    
    try:
        os.makedirs(args.output_dir, exist_ok=True)
        test_file = os.path.join(args.output_dir, 'test_write.tmp')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        return True
    except Exception as e:
        print(f"Ошибка доступа к директории {args.output_dir}: {e}")
        return False


def main() -> None:
    """Главная функция программы."""
    try:
        args = parse_arguments()
        
        if not validate_arguments(args):
            sys.exit(1)
        
        print("Программа для скачивания аудиофайлов")
        print(f"Папка для файлов: {args.output_dir}")
        print(f"Файл аннотации: {args.csv_path}")
        print(f"Количество файлов: {args.count}")
        print("Инструменты: trumpet, ukulele, harp")
        
        audio_manager = AudioManager(args.output_dir, args.csv_path)
        
        downloaded_count = audio_manager.download_audio_collection(args.count)
        
        if downloaded_count > 0:
            if audio_manager.create_annotation():
                audio_manager.demonstrate_iterator()
                print(f"Программа успешно завершена!")
                print(f"Скачано файлов: {downloaded_count}")
            else:
                print("Не удалось создать аннотацию")
                sys.exit(1)
        else:
            print("Не удалось скачать файлы")
            sys.exit(1)

    except KeyboardInterrupt:
        print("Программа прервана пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()