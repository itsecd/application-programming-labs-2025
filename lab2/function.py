'''
Функции обработки файлов
'''
import argparse
from pathlib import Path
from file_path_iterator import FilePathIterator
from parsing import fetch_audio_urls, download_audio_files, save_annotation

INSTRUMENTS: list[str] = ['trumpet', 'ukulele', 'harp']

def count_files(lst: list[list[str]]) -> int:
    """Вычислить количество скаченных файлов
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
            print(f"Имя файла: {filename}"
                  f" Относительный путь: {rel_path};"
                  f" Абсолютный путь: {abs_path}")
    except FileNotFoundError:
        print(f"Файл {csv_path} не найден")
    except OSError as e:
        print(f"Ошибка чтения файла '{csv_path}': {e}")

def main() -> None:
    """
    Основная функция для скачивания аудиофайлов.
    """
    try:
        parser = argparse.ArgumentParser(description='Обработка данных пользователей')
        parser.add_argument('save_directory', type=str,
                            help='Путь к директории для сохранения файлов')
        parser.add_argument('-a', '--annotation',
            type=str, help='Путь к файлу аннотоции',
            default=None)
        args = parser.parse_args()
        save_dir = args.save_directory
        if save_dir is None:
            save_dir = Path.cwd()
        else:
            save_dir = Path(args.save_directory)
        print("Получение URL аудиофайлов...")
        audio_map: dict[str, list[str]] = {}
        all_urls: list[list[str]] = []
        for instrument in INSTRUMENTS:
            urls = fetch_audio_urls(instrument)
            audio_map[instrument] = urls
            all_urls.append(urls)
        count_audio = count_files(all_urls)
        print("Скачивание аудиофайлов...")
        all_data: list[list[str]] = []
        for instrument in INSTRUMENTS:
            data = download_audio_files(
                instrument,
                audio_map[instrument],
                count_audio,
                save_dir
            )
            all_data.extend(data)
        csv_path = args.annotation
        if csv_path is None:
            csv_path = save_dir / 'annotation.csv'
        else:
            csv_path = Path(args.annotation)
        save_annotation(all_data, csv_path)
        print_annotation(csv_path)
    except Exception as e:
        print(f"Критическая ошибка в main(): {e}")
        raise
