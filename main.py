import argparse
from typing import Optional
import os
import csv
import time
import requests
from bs4 import BeautifulSoup

class FilePathIterator:
    def __init__(self, annotation = Optional[None], output_dir = Optional[None]) -> Optional[None]:
        """
        Итератор по путям к файлам
        :param annotation_file: путь к .csv файлу с аннотацией
        :param folder_path: путь к папке с файлами
        """
        self.paths = []
        self.index = 0
        
        if annotation:
            with open(annotation, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if row:
                        self.paths.append(row[0])
        
        elif output_dir:
            absolute_path = os.path.abspath(output_dir)
            for filename in os.listdir(absolute_path):
                if filename.endswith('.mp3'):
                    full_path = os.path.join(absolute_path, filename)
                    self.paths.append(full_path)
        
        else:
            raise ValueError("Не указан параметр")

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        else:
            raise StopIteration


def download_audio_file(url: str, filename: str, output_dir: str) -> Optional[str]:
    """
    Скачивание аудиофайла.
    """

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        page = requests.get(url, headers=headers)
        
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(page.content)
        
        return filepath

    except Exception as e:
        print(f"Ошибка при скачивании {filename}: {e}")
        return None


def parsing_site(base_url: str, genre: str, count_per_genre: int) -> list[str]:
    """
    Нахождение ссылок с файлами нужного жанраю
    """

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    
    audio_links = []
    genre_url = f"{base_url}/{genre}/"
    
    while len(audio_links) < count_per_genre:        
        try:
            page = requests.get(genre_url, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            
            audio_players = soup.find_all('div', {'data-audio-player-preview-url-value': True})
            for player in audio_players:
                if len(audio_links) >= count_per_genre:
                    break
                    
                audio_url = player.get('data-audio-player-preview-url-value')
                if audio_url and audio_url.startswith('http'):
                    audio_links.append(audio_url)
                    print(f"Ссылка на файл успешно сохранена")
            
           
        except Exception as e:
            print(f"Ошибка при парсинге страницы для жанра {genre}: {e}")
            break
    
    return audio_links[:count_per_genre]


def create_annotation(audio_files: list[tuple[str, str]], output_dir: str, annotation: str, genre: str) -> None:
    """
    Создание .csv файла.
    """

    file_exists = os.path.exists(annotation)
    mode = 'a' if file_exists else 'w'

    with open(annotation, mode, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(['Абсолютный путь', 'Относительный путь', 'Жанр'])
        
        for absolute_path, relative_path in audio_files:
            writer.writerow([absolute_path, relative_path, genre])
    


def main():
    parser = argparse.ArgumentParser(description='Скачивание аудиофайлов с mixkit.co')
    parser.add_argument('output_dir', type=str, help='Путь к папке с сохраненными файлами')
    parser.add_argument('annotation', type=str, help='Путь к файлу с аннотацией')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    
    genres = ['rock', 'jazz', 'contemporary-r-and-b']
    files_per_genre = 5
    
    base_url = 'https://mixkit.co/free-stock-music'
    all_audio_files = []
    
    for genre in genres:
        audio_urls = parsing_site(base_url, genre, files_per_genre)
        
        for i, audio_url in enumerate(audio_urls):
            try:
                filename = f"{genre}_{i+1}.mp3"
                filepath = download_audio_file(audio_url, filename, args.output_dir)
                
                if filepath:
                    relative_path = os.path.relpath(filepath, args.output_dir)
                    absolute_path = os.path.abspath(filepath)
                    all_audio_files.append((absolute_path, relative_path))
                
            except Exception as e:
                print(f"Ошибка при обработке файла {i+1} для жанра {genre}: {e}")

        create_annotation(all_audio_files, args.output_dir, args.annotation, genre)


    

if __name__ == "__main__":
    main()
