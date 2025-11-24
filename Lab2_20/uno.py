"""
Главный модуль программы для скачивания звуков транспорта с созданием аннотации.
"""

import argparse
import csv
import os
import sys
from typing import List

from tri import AudioDownloader
from due import AudioIterator


class TransportAudioManager:
    """Менеджер для управления процессом скачивания звуков транспорта и создания аннотации."""

    def __init__(self, download_dir: str, annotation_file: str):
        """Инициализация менеджера с указанием директории и файла аннотации."""
        self.download_dir = download_dir
        self.annotation_file = annotation_file
        self.downloader = AudioDownloader(download_dir)

    def download_transport_sounds(self, total_count: int) -> int:
        """Скачивает коллекцию звуков транспорта."""
        print("Начинаем скачивание звуков транспорта...")
        print(f"Планируемое количество файлов: {total_count}")

        downloaded_count = self.downloader.download_transport_audio(total_count)
        
        print(f"Успешно скачано: {downloaded_count}/{total_count}")
        return downloaded_count

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
            print("\nДемонстрация работы итератора:")

            if not os.path.exists(self.annotation_file):
                print("Файл аннотации не найден")
                return

            iterator = AudioIterator(self.annotation_file)

            print(f"Всего файлов в аннотации: {len(iterator)}")
            print("Первые 5 файлов:")

            for i, filepath in enumerate(iterator):
                if i < 5:
                    file_info = iterator.get_file_info(filepath)
                    print(f"  {i + 1}. {file_info['filename']} ({file_info['file_size']} bytes)")
                
            if len(iterator) > 5:
                print(f"  ... и еще {len(iterator) - 5} файлов")

        except Exception as e:
            print(f"Ошибка демонстрации итератора: {e}")


def parse_arguments():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description='Скачивание звуков транспорта с сайта mixkit.co с созданием аннотации'
    )

    parser.add_argument('--output_dir', required=True, 
                       help='Путь к папке для сохранения звуков транспорта')
    parser.add_argument('--csv_path', required=True, 
                       help='Путь к файлу для CSV аннотации')
    parser.add_argument('--count', type=int, default=60, 
                       choices=range(50, 1001),
                       help='Общее количество файлов для скачивания (50-1000)')

    return parser.parse_args()


def validate_arguments(args) -> bool:
    """Проверяет корректность аргументов командной строки."""
    if not (50 <= args.count <= 1000):
        print("Ошибка: количество файлов должно быть от 50 до 1000")
        return False

    try:
        os.makedirs(args.output_dir, exist_ok=True)
        # Проверяем возможность записи в директорию
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

        print("=== ПРОГРАММА ДЛЯ СКАЧИВАНИЯ ЗВУКОВ ТРАНСПОРТА ===")
        print(f"Папка для файлов: {args.output_dir}")
        print(f"Файл аннотации: {args.csv_path}")
        print(f"Количество файлов: {args.count}")

        audio_manager = TransportAudioManager(args.output_dir, args.csv_path)

        # Скачиваем звуки транспорта
        downloaded_count = audio_manager.download_transport_sounds(args.count)

        if downloaded_count >= 50:  # Минимум 50 файлов
            if audio_manager.create_annotation():
                audio_manager.demonstrate_iterator()
                print(f"\n Программа успешно завершена!")
                print(f"Скачано звуков транспорта: {downloaded_count}")
            else:
                print(" Не удалось создать аннотацию")
                sys.exit(1)
        else:
            print(f" Скачано недостаточно файлов: {downloaded_count} (требуется минимум 50)")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
        sys.exit(1)
    except Exception as e:
        print(f" Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
    #python D:\application-programming-labs-2025\Lab2_20\uno.py --output_dir ./sounds --csv_path ./annotation.csv --count 50