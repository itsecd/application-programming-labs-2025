"""
Модуль с итератором для работы с путями к аудиофайлам.
"""

import os
import csv
from typing import Iterator, List


class AudioIterator:
    """Итератор для перебора путей к аудиофайлам."""
    
    def __init__(self, source: str):
        """Инициализация итератора с указанием источника данных."""
        self.source = source   #путь к CSV файлу или папке с MP3 файлами
        self._paths: List[str] = []  #список для хранения всех путей к файлам
        self._index: int = 0
        self._load_paths()

    def _load_paths(self) -> None:
        """Загружает пути к файлам из указанного источника."""
        if os.path.isfile(self.source) and self.source.endswith('.csv'): #если источник - CSV файл
            self._load_paths_from_csv()
        elif os.path.isdir(self.source):
            self._load_paths_from_directory()
        else:
            raise ValueError("Источник должен быть CSV файлом или директорией")

    def _load_paths_from_csv(self) -> None:
        """Загружает пути из CSV файла аннотации."""
        try:
            with open(self.source, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                if 'absolute_path' not in reader.fieldnames:
                    raise ValueError("CSV файл должен содержать колонку 'absolute_path'")
                
                for row in reader:
                    file_path = row['absolute_path']
                    if os.path.exists(file_path):
                        self._paths.append(file_path)
            
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV файл не найден: {self.source}")
        except Exception as e:
            raise Exception(f"Ошибка чтения CSV файла: {e}")

    def _load_paths_from_directory(self) -> None:
        """Загружает пути из директории с файлами."""
        if not os.path.exists(self.source): #проверяем что папка существует
            raise FileNotFoundError(f"Директория не найдена: {self.source}")
        #os.walk рекурсивно обходит все папки и файлы в указанной директории
        try:
            for root, _, files in os.walk(self.source): #root - текущая папка, files - список файлов в ней
                for filename in files:
                    if filename.lower().endswith('.mp3'):
                        file_path = os.path.join(root, filename)  #создание полного пути к файлу
                        if os.path.isfile(file_path):  #проверка действительно файл (а не папка)
                            self._paths.append(os.path.abspath(file_path))
            
        except Exception as e:
            raise Exception(f"Ошибка чтения директории: {e}")

    def __iter__(self) -> Iterator[str]:
        """Возвращает итератор для перебора файлов."""
        self._index = 0
        return self #возвращает сам объект как итератор

    def __next__(self) -> str:
        """Возвращает следующий путь к файлу."""
        if self._index < len(self._paths): #если еще есть файлы для перебора
            path = self._paths[self._index]
            self._index += 1
            return path
        raise StopIteration

    def __len__(self) -> int:
        """Возвращает количество файлов."""
        return len(self._paths)

    def get_file_info(self, file_path: str) -> dict:
        """Возвращает информацию о файле."""
        try:
            return {
                'filename': os.path.basename(file_path), #имя файла без пути (song.mp3)
                'absolute_path': os.path.abspath(file_path),
                'relative_path': os.path.relpath(file_path),
                'file_size': os.path.getsize(file_path) if os.path.exists(file_path) else 0
            }
        except Exception:
            return {
                'filename': os.path.basename(file_path),
                'absolute_path': file_path,
                'relative_path': file_path,
                'file_size': 0
            }