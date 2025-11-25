# cd /d D:\Projects\application-programming-labs-2025
import argparse
import os
import csv
import requests
import time
from bs4 import BeautifulSoup



class FilePathIterator:
    def __init__(self, annotation=None, output_dir=None):
        """
        Итератор по путям к файлам
        :param annotation_file: путь к CSV файлу с аннотацией
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


def download_audio_file(url, filename, output_dir):
    """Скачивает аудиофайл и сохраняет его"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        response = requests.get(url, headers=headers)
        
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"Успешно скачан: {filename} ({len(response.content)} байт)")
        return filepath
    except Exception as e:
        print(f"Ошибка при скачивании {filename}: {e}")
        return None


def parsing_site(base_url, genre, count_per_genre):
    """Парсит сайт и возвращает ссылки на аудиофайлы"""
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    
    audio_links = []
    genre_url = os.path.join(base_url, genre)
    
    while len(audio_links) < count_per_genre:        
        try:
            response = requests.get(genre_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            audio_players = soup.find_all('div', {'data-audio-player-preview-url-value': True})
            
            for player in audio_players:
                if len(audio_links) >= count_per_genre:
                    break
                    
                audio_url = player.get('data-audio-player-preview-url-value')
                if audio_url and audio_url.startswith('http'):
                    audio_links.append(audio_url)
            
           
        except Exception as e:
            print(f"Ошибка при парсинге страницы для жанра {genre}: {e}")
            break
    
    return audio_links[:count_per_genre]


def create_annotation(audio_files, output_dir, annotation):
    """Создает CSV файл с аннотацией"""
    with open(annotation, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Абсолютный путь', 'Относительный путь', 'Жанр', 'Композитор'])
        
        for absolute_path, relative_path in audio_files:
            writer.writerow([absolute_path, relative_path])
    


def main():
    parser = argparse.ArgumentParser(description='Скачивание аудиофайлов с mixkit.co')
    parser.add_argument('output_dir', type=str, help='Путь к папке с сохраненными файлами')
    parser.add_argument('annotation', type=str, help='Путь к файлу с аннотацией')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    
    genres = ['rock', 'jazz', 'r-b']
    files_per_genre = 20
    
    base_url = 'https://mixkit.co/free-stock-music'
    all_audio_files = []
    
    for genre in genres:
        audio_urls = parsing_site(base_url, genre, files_per_genre)
        
        for i, audio_url in enumerate(audio_urls):
            try:
                filepath = download_audio_file(audio_url, audio_url, args.output_dir)
                
                if filepath:
                    relative_path = os.path.relpath(filepath, args.output_dir)
                    all_audio_files.append((filepath, relative_path))
                
            except Exception as e:
                print(f"Ошибка при обработке файла {i+1} для жанра {genre}: {e}")

        create_annotation(all_audio_files, args.output_dir, args.annotation)
    

if __name__ == "__main__":
    main()
