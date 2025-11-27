from pathlib import Path
import csv
from FilePathIterator import FilePathIterator
from Parsing import fetch_audio_urls, download_audio_files, save_annotation

INSTRUMENTS: list[str] = ['trumpet', 'ukulele', 'harp']

def count(lst: list[list[str]]) -> int:
    """Вычислить количество скаченных файлов.
    :param lst: Список всех ссылок на скачивание.
    """
    count = 0
    for sublist in lst:
        if count == 0:
            count = len(sublist)
        else:
            count = min(count, len(sublist))
    return count

def print_annotation(csv_path: Path) -> None:
    """
    Вывести содержимое аннотации через итератор.

    :param csv_path: Путь к CSV-файлу.
    """
    print("\n--- Чтение аннотации через FilePathIterator ---")
    try:
        iterator = FilePathIterator(str(csv_path))
        for filename, abs_path, rel_path in iterator:
            print(f"Имя файла: {filename} Относительный путь: {rel_path}; Абсолютный путь: {abs_path}")
    except Exception as e:
        print(f"Ошибка итератора: {e}")

def main() -> None:
    """
    Основная функция для скачивания аудиофайлов.

    Последовательно:
    1. Получает URL для каждого инструмента
    2. Определяет максимальное количество файлов
    3. Скачивает аудиофайлы
    4. Сохраняет аннотацию в CSV
    5. Выводит загруженные файлы
    """
    try:
        script_dir = Path(__file__).parent

        print("Получение URL аудиофайлов...")
        audio_map: dict[str, list[str]] = {}
        all_urls: list[list[str]] = []

        for instrument in INSTRUMENTS:
            urls = fetch_audio_urls(instrument)
            audio_map[instrument] = urls
            all_urls.append(urls)

        count_audio = count(all_urls)
        
        print("Скачивание аудиофайлов...")
        all_data: list[list[str]] = []
        for instrument in INSTRUMENTS:
            data = download_audio_files(
                instrument,
                audio_map[instrument],
                count_audio,
                script_dir
            )
            all_data.extend(data)

        csv_path = script_dir / 'data.csv'
        save_annotation(all_data, csv_path)

        print_annotation(csv_path)

    except Exception as e:
        print(f"Критическая ошибка в main(): {e}")
        raise

