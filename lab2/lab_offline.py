import os
import csv
import argparse
from pathlib import Path
from typing import Iterator, List, Dict, Any

class AudioFileIterator:
    """Итератор по абсолютным путям аудиофайлов из CSV-аннотации.

    Читает CSV-файл с колонкой 'absolute_path' и возвращает пути по одному.
    Корректно управляет ресурсами: открывает файл при начале итерации
    и закрывает его при завершении (включая досрочное прерывание через break).
    Поддерживает однократное использование в рамках одного цикла for.
    """

    def __init__(self, annotation_path: str | Path) -> None:
        """Инициализирует итератор с путём к CSV-файлу аннотации.

        Args:
            annotation_path (str | Path): Путь к CSV-файлу с аннотацией.
        """
        self.annotation_path = Path(annotation_path)
        self._file = None      # Файловый дескриптор (будет открыт в __iter__)
        self._reader = None    # CSV-ридер для построчного чтения

    def __iter__(self) -> 'AudioFileIterator':
        """Создаёт итератор: открывает CSV-файл и инициализирует DictReader.

        Возвращает сам объект, который выступает в роли итератора.
        Файл открывается заново при каждом вызове __iter__ (например, при for).

        Returns:
            AudioFileIterator: Текущий экземпляр, готовый к итерации.
        """
        self._file = open(self.annotation_path, 'r', encoding='utf-8', newline='')
        self._reader = csv.DictReader(self._file)
        return self

    def __next__(self) -> str:
        """Возвращает абсолютный путь к следующему аудиофайлу из CSV.

        Извлекает значение из колонки 'absolute_path' текущей строки.
        При достижении конца файла закрывает ресурсы и вызывает StopIteration.

        Returns:
            str: Абсолютный путь к аудиофайлу.

        Raises:
            StopIteration: Когда все строки обработаны.
            KeyError: Если в CSV отсутствует колонка 'absolute_path'.
        """
        if self._reader is None:
            # Защита от повторного использования после завершения итерации
            raise StopIteration

        try:
            row = next(self._reader)
            return row['absolute_path']
        except StopIteration:
            # Закрываем файл при естественном завершении итерации
            if self._file and not self._file.closed:
                self._file.close()
            self._file = None
            self._reader = None
            raise

    def __del__(self) -> None:
        """Деструктор: обеспечивает закрытие файла при уничтожении объекта.

        Срабатывает, если итерация была прервана досрочно (например, break)
        и файл остался открытым. Это страховка против утечки файловых дескрипторов.
        """
        if self._file and not self._file.closed:
            self._file.close()


def generate_audio_files(output_dir: Path, max_num: int) -> List[Dict[str, str]]:
    """Создаёт пустые .mp3-файлы для имитации скачанных треков.

    Генерирует файлы вида pop_track_001.mp3 ... pop_track_{max_num}.mp3,
    записывает в них минимальный валидный ID3-заголовок,
    и возвращает данные для аннотации.

    Args:
        output_dir (Path): Директория для сохранения файлов.
        max_num (int): Количество файлов для генерации.

    Returns:
        List[Dict[str, str]]: Список записей с absolute_path и relative_path.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    annotation_data: List[Dict[str, str]] = []

    print(f"🚀 Создание {max_num} тестовых аудиофайлов в жанре 'pop'...")

    for i in range(1, max_num + 1):
        filename = f"pop_track_{i:03d}.mp3"
        filepath = output_dir / filename

        # Создаём пустой .mp3-файл с минимальным ID3-заголовком
        with open(filepath, 'wb') as f:
            f.write(b'\x49\x44\x33\x03\x00\x00\x00\x00\x00\x00')  # ID3v2.3 empty header

        abs_path = str(filepath.resolve())
        rel_path = str(filepath.relative_to(output_dir.parent))

        annotation_data.append({
            'absolute_path': abs_path,
            'relative_path': rel_path
        })

        if i <= 5:
            print(f"✅ Создан: {filename}")

    print(f"🎉 Готово: {max_num} файлов создано.")
    return annotation_data


def save_annotation(annotation_data: List[Dict[str, str]], annotation_file: Path) -> None:
    """Сохраняет аннотацию в CSV-файл с колонками absolute_path и relative_path.

    Args:
        annotation_data (List[Dict[str, str]]): Данные для записи.
        annotation_file (Path): Путь к выходному CSV-файлу.
    """
    annotation_file.parent.mkdir(parents=True, exist_ok=True)
    with open(annotation_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['absolute_path', 'relative_path'])
        writer.writeheader()
        writer.writerows(annotation_data)


def main() -> None:
    """Основная функция: парсит аргументы, генерирует файлы, сохраняет аннотацию и демонстрирует итератор."""
    parser = argparse.ArgumentParser(
        description="Оффлайн-версия: генерация тестовых аудиофайлов и аннотации (жанр pop)"
    )
    parser.add_argument(
        '--output_dir', type=str, required=True,
        help="Путь к папке для сохранения аудиофайлов (например: ./audio/pop)"
    )
    parser.add_argument(
        '--annotation_file', type=str, required=True,
        help="Путь к CSV-файлу аннотации (например: ./annotations/pop_tracks.csv)"
    )
    parser.add_argument(
        '--max_num', type=int, default=100,
        help="Количество тестовых файлов (от 50 до 1000)"
    )

    args = parser.parse_args()

    if not (50 <= args.max_num <= 1000):
        parser.error("--max_num должно быть в диапазоне от 50 до 1000.")

    output_dir = Path(args.output_dir)
    annotation_file = Path(args.annotation_file)

    print("🚀 Запуск оффлайн-лабораторной работы...")
    annotation_data = generate_audio_files(output_dir, args.max_num)

    save_annotation(annotation_data, annotation_file)
    print(f"📄 Аннотация сохранена: {annotation_file}")

    print("\n🔍 Демонстрация итератора (первые 3 файла):")
    iterator = AudioFileIterator(annotation_file)
    count = 0
    for path in iterator:
        print(path)
        count += 1
        if count >= 3:
            break

    print("\n🎉 Лабораторная работа успешно завершена (оффлайн-режим)!")


if __name__ == '__main__':
    main()