import csv
import os
import requests
import random
import argparse
from bs4 import BeautifulSoup


class AudioIterator:
    """
    Итератор для чтения абсолютных путей из CSV файла.
    
    Args:
        csv_file (str): Путь к CSV файлу с аннотацией
    """
    
    def __init__(self, csv_file: str) -> None:
        self.data = []
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                self.data.append(row[0])
        self.index = 0
    
    def __iter__(self) -> 'AudioIterator':
        return self
    
    def __next__(self) -> str:
        if self.index < len(self.data):
            path = self.data[self.index]
            self.index += 1
            return path
        raise StopIteration


def download_audio(save_dir: str, annotation_file: str, count: int = 50) -> int:
    """
    Скачивает аудиофайлы с сайта mixkit.co и создает CSV аннотацию.
    
    Args:
        save_dir (str): Папка для сохранения файлов
        annotation_file (str): Файл для аннотации
        count (int): Количество файлов для скачивания
    
    Returns:
        int: Количество скачанных файлов
    """
    instruments = ['flute', 'violin', 'drums']
    counts = [1, 1, 1]
    
    for _ in range(count - 3):
        counts[random.randint(0, 2)] += 1
    
    print(f"Скачаем: флейта={counts[0]}, скрипка={counts[1]}, барабаны={counts[2]}")
    
    os.makedirs(save_dir, exist_ok=True)
    annotation = []
    downloaded = 0
    
    for instrument, need_count in zip(instruments, counts):
        print(f"Ищем {instrument}...")
        
        url = f"https://mixkit.co/free-stock-music/instrument/{instrument}/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            tracks = soup.find_all("div", class_="item-grid-card")
            
            for track in tracks[:need_count]:
                audio_div = track.find("div", attrs={"data-audio-player-preview-url-value": True})
                if audio_div:
                    audio_url = audio_div.get("data-audio-player-preview-url-value")
                    if audio_url:
                        filename = f"{instrument}_{downloaded + 1}.mp3"
                        abs_path = os.path.abspath(os.path.join(save_dir, filename))
                        rel_path = os.path.join(save_dir, filename)
                        
                        audio_data = requests.get(audio_url)
                        audio_data.raise_for_status()
                        
                        with open(abs_path, 'wb') as file:
                            file.write(audio_data.content)
                        
                        annotation.append([abs_path, rel_path])
                        downloaded += 1
                        print(f"Скачано: {filename}")
                        
        except requests.RequestException as e:
            print(f"Ошибка сети с {instrument}: {e}")
        except Exception as e:
            print(f"Ошибка с {instrument}: {e}")
    
    try:
        with open(annotation_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['absolute_path', ' relative_path'])
            for row in annotation:
                # Форматируем строку с пробелом после запятой
                file.write(f"{row[0]}, {row[1]}\n")
    except IOError as e:
        print(f"Ошибка записи CSV: {e}")
        return downloaded
    
    print(f"Готово! Скачано {downloaded} файлов")
    return downloaded


def main() -> None:
    """Основная функция программы."""
    parser = argparse.ArgumentParser(
        description='Скачивание аудиофайлов с mixkit.co'
    )
    parser.add_argument(
        '--save_dir', 
        required=True, 
        help='Папка для сохранения файлов'
    )
    parser.add_argument(
        '--annotation', 
        required=True, 
        help='Файл для аннотации'
    )
    parser.add_argument(
        '--count', 
        type=int, 
        default=50, 
        help='Количество файлов для скачивания'
    )
    
    args = parser.parse_args()
    
    try:
        download_audio(args.save_dir, args.annotation, args.count)
        
        print("\nПроверка итератора:")
        iterator = AudioIterator(args.annotation)
        for i, path in enumerate(iterator):
            print(f"{i + 1}: {path}")
            if i >= 3:
                break
                
    except Exception as e:
        print(f"Критическая ошибка: {e}")


if __name__ == "__main__":
    main()
