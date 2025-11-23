import requests
from bs4 import BeautifulSoup
import csv
import time
import argparse
from urllib.parse import urljoin
from pathlib import Path
import mutagen
import re

class AudioFileDownloader:
    def __init__(self, download_dir):
        self.base_url = "https://mixkit.co"
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)
    
    def get_headers(self):
        """Получить общие headers для всех запросов"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://mixkit.co/'
        }
    
    def get_theme_categories(self):
        """Получить список тем из раздела Sound Effects"""
        themes = [
            {'name': 'Transition', 'url': self.base_url + '/free-sound-effects/transition/'},
            {'name': 'Nature', 'url': self.base_url + '/free-sound-effects/nature/'},
            {'name': 'Animals', 'url': self.base_url + '/free-sound-effects/animals/'},
            {'name': 'Human', 'url': self.base_url + '/free-sound-effects/human/'},
            {'name': 'Cartoon', 'url': self.base_url + '/free-sound-effects/cartoon/'},
            {'name': 'Impacts', 'url': self.base_url + '/free-sound-effects/impacts/'},
            {'name': 'Magic', 'url': self.base_url + '/free-sound-effects/magic/'},
            {'name': 'Weather', 'url': self.base_url + '/free-sound-effects/weather/'},
            {'name': 'Instruments', 'url': self.base_url + '/free-sound-effects/instruments/'},
            {'name': 'Office', 'url': self.base_url + '/free-sound-effects/office/'},
            {'name': 'Household', 'url': self.base_url + '/free-sound-effects/household/'},
            {'name': 'Science', 'url': self.base_url + '/free-sound-effects/science/'},
            {'name': 'Transportation', 'url': self.base_url + '/free-sound-effects/transportation/'},
            {'name': 'Alarms', 'url': self.base_url + '/free-sound-effects/alarms/'},
            {'name': 'Bells', 'url': self.base_url + '/free-sound-effects/bells/'},
            {'name': 'Click', 'url': self.base_url + '/free-sound-effects/click/'},
            {'name': 'Notification', 'url': self.base_url + '/free-sound-effects/notification/'},
            {'name': 'UI', 'url': self.base_url + '/free-sound-effects/ui/'},
            {'name': 'Game', 'url': self.base_url + '/free-sound-effects/game/'},
            {'name': 'Footsteps', 'url': self.base_url + '/free-sound-effects/footsteps/'},
            {'name': 'Whoosh', 'url': self.base_url + '/free-sound-effects/whoosh/'},
            {'name': 'Swoosh', 'url': self.base_url + '/free-sound-effects/swoosh/'},
            {'name': 'Sci-fi', 'url': self.base_url + '/free-sound-effects/sci-fi/'},
            {'name': 'Horror', 'url': self.base_url + '/free-sound-effects/horror/'},
            {'name': 'Sports', 'url': self.base_url + '/free-sound-effects/sports/'},
            {'name': 'Water', 'url': self.base_url + '/free-sound-effects/water/'},
            {'name': 'Fire', 'url': self.base_url + '/free-sound-effects/fire/'},
            {'name': 'Wind', 'url': self.base_url + '/free-sound-effects/wind/'},
            {'name': 'Rain', 'url': self.base_url + '/free-sound-effects/rain/'},
            {'name': 'Thunder', 'url': self.base_url + '/free-sound-effects/thunder/'},
        ]
        return themes
    
    def parse_duration(self, duration_text):
        """Парсинг длительности из текста"""
        try:
            if ':' in duration_text:
                parts = duration_text.strip().split(':')
                if len(parts) == 2:
                    return int(parts[0]) * 60 + int(parts[1])
                elif len(parts) == 3:
                    return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        except:
            pass
        return 0
    
    def get_audio_links_from_theme(self, theme_url, max_links):
        """Получить ссылки на аудио из конкретной темы"""
        audio_items = []
        page = 1
        
        while len(audio_items) < max_links and page <= 5:
            try:
                url = theme_url if page == 1 else f"{theme_url}?page={page}"
                
                response = requests.get(url, headers=self.get_headers(), timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                audio_cards = soup.find_all('div', class_='item-grid-card')
                
                for card in audio_cards:
                    if len(audio_items) >= max_links:
                        break
                    
                    duration_element = card.find('div', class_='item-grid-sfx-preview__meta-time')
                    if duration_element:
                        duration_text = duration_element.get_text(strip=True)
                        duration_seconds = self.parse_duration(duration_text)
                        
                        if duration_seconds >= 10:
                            download_button = card.find('button', class_='download-button--icon')
                            if download_button:
                                item_id = download_button.get('data-algolia-analytics-item-id')
                                download_path = download_button.get('data-download--button-modal-url-value')
                                
                                if item_id and download_path:
                                    download_url = urljoin(self.base_url, download_path)
                                    title_element = card.find('h3') or card.find('h4') or card.find('a')
                                    title = title_element.get_text(strip=True) if title_element else f"audio_{item_id}"
                                    
                                    audio_items.append({
                                        'item_id': item_id,
                                        'download_url': download_url,
                                        'duration': duration_seconds,
                                        'title': title
                                    })
                
                page += 1
                time.sleep(0.5)
                
            except Exception:
                break
        
        return audio_items[:max_links]
    
    def get_final_download_url(self, download_url):
        """Получить финальную ссылку для скачивания"""
        try:
            response = requests.get(download_url, headers=self.get_headers(), timeout=15, allow_redirects=True)
            response.raise_for_status()
            
            if response.history:
                return response.url
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            audio_link = soup.find('a', href=lambda x: x and any(ext in x.lower() for ext in ['.mp3', '.wav', '.ogg']))
            if audio_link:
                return urljoin(download_url, audio_link['href'])
            
            audio_tag = soup.find('audio')
            if audio_tag and audio_tag.get('src'):
                return urljoin(download_url, audio_tag['src'])
            
            return download_url
            
        except Exception:
            return None
    
    def get_audio_links(self, num_files=1000):
        """Получить ссылки на аудиофайлы из разных тем"""
        audio_links = []
        themes = self.get_theme_categories()
        links_per_theme = max(3, num_files // len(themes))
        
        print(f"Поиск {num_files} файлов в {len(themes)} темах...")
        
        for theme in themes:
            if len(audio_links) >= num_files:
                break
                
            audio_items = self.get_audio_links_from_theme(theme['url'], links_per_theme)
            
            for item in audio_items:
                if len(audio_links) >= num_files:
                    break
                
                final_url = self.get_final_download_url(item['download_url'])
                if final_url:
                    audio_links.append({
                        'url': final_url,
                        'item_id': item['item_id'],
                        'title': item['title']
                    })
                
                time.sleep(0.3)
        
        return audio_links[:num_files]
    
    def download_audio_files(self, num_files=1000):
        """Скачать аудиофайлы"""
        audio_links = self.get_audio_links(num_files)
        
        if not audio_links:
            print("Не найдено подходящих файлов")
            return []
        
        print(f"Скачивание {len(audio_links)} файлов...")
        downloaded_files = []
        
        for i, audio_info in enumerate(audio_links, 1):
            try:
                audio_url = audio_info['url']
                item_id = audio_info['item_id']
                title = audio_info['title']
                
                safe_title = re.sub(r'[^\w\s-]', '', title)
                safe_title = re.sub(r'[-\s]+', '-', safe_title)
                safe_title = safe_title.strip('-_')[:50]
                
                file_extension = 'mp3'
                for ext in ['.mp3', '.wav', '.ogg']:
                    if ext in audio_url.lower():
                        file_extension = ext[1:]
                        break
                
                filename = f"{safe_title}_{item_id}.{file_extension}"
                filepath = self.download_dir / filename
                
                if filepath.exists():
                    downloaded_files.append(filepath)
                    continue
                
                print(f"{i}/{len(audio_links)}: {filename}")
                
                response = requests.get(audio_url, headers=self.get_headers(), stream=True, timeout=60)
                response.raise_for_status()
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                if filepath.exists() and filepath.stat().st_size > 1000:
                    downloaded_files.append(filepath)
                
                time.sleep(1)
                
            except Exception:
                continue
        
        print(f"Скачано: {len(downloaded_files)} файлов")
        return downloaded_files
    
    def get_audio_duration_from_file(self, filepath):
        """Получить длительность аудиофайла"""
        try:
            audio = mutagen.File(filepath)
            if audio and hasattr(audio.info, 'length'):
                return audio.info.length
        except:
            pass
        return None
    
    def create_annotation_csv(self, audio_files, annotation_file):
        """Создать CSV-файл с аннотацией"""
        annotation_path = Path(annotation_file)
        annotation_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(annotation_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['absolute_path', 'relative_path', 'filename', 'duration_seconds', 'file_size_mb'])
            
            for audio_file in audio_files:
                try:
                    absolute_path = str(audio_file.resolve())
                    
                    try:
                        relative_path = str(audio_file.relative_to(Path.cwd()))
                    except ValueError:
                        relative_path = absolute_path
                    
                    filename = audio_file.name
                    duration = self.get_audio_duration_from_file(audio_file) or 0
                    file_size_mb = audio_file.stat().st_size / (1024 * 1024)
                    
                    writer.writerow([absolute_path, relative_path, filename, f"{duration:.1f}", f"{file_size_mb:.2f}"])
                except Exception:
                    continue
        
        print(f"Аннотация создана: {annotation_file}")

class AudioFileIterator:
    """Итератор по путям к аудиофайлам"""
    
    def __init__(self, source):
        self.file_paths = []
        
        if isinstance(source, str):
            source_path = Path(source)
            
            if source_path.is_file() and source_path.suffix.lower() == '.csv':
                self._load_from_csv(source_path)
            elif source_path.is_dir():
                self._load_from_directory(source_path)
        
        self.index = 0
    
    def _load_from_csv(self, csv_path):
        """Загрузить пути из CSV-файла"""
        try:
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if 'absolute_path' in row and row['absolute_path']:
                        file_path = Path(row['absolute_path'])
                        if file_path.exists():
                            self.file_paths.append(row['absolute_path'])
        except Exception:
            pass
    
    def _load_from_directory(self, directory_path):
        """Загрузить пути из папки"""
        audio_extensions = {'.mp3', '.wav', '.ogg', '.m4a'}
        
        for file_path in directory_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in audio_extensions:
                self.file_paths.append(str(file_path.resolve()))
    
    def __iter__(self):
        self.index = 0
        return self
    
    def __next__(self):
        if self.index < len(self.file_paths):
            file_path = self.file_paths[self.index]
            self.index += 1
            return file_path
        else:
            raise StopIteration
    
    def __len__(self):
        return len(self.file_paths)

def main():
    parser = argparse.ArgumentParser(description='Скачивание аудиофайлов из Mixkit')
    parser.add_argument('--download-dir', '-d', required=True, help='Папка для сохранения')
    parser.add_argument('--annotation-file', '-a', required=True, help='Файл аннотации')
    parser.add_argument('--num-files', '-n', type=int, default=100, help='Количество файлов')
    parser.add_argument('--use-iterator', '-i', action='store_true', help='Запустить итератор')
    
    args = parser.parse_args()
    
    download_dir = Path(args.download_dir).resolve()
    annotation_file = Path(args.annotation_file).resolve()
    
    downloader = AudioFileDownloader(download_dir)
    
    print("Скачивание аудиофайлов >10 секунд")
    print(f"Папка: {download_dir}")
    print(f"Количество: {args.num_files} файлов")
    
    downloaded_files = downloader.download_audio_files(args.num_files)
    
    if downloaded_files:
        downloader.create_annotation_csv(downloaded_files, annotation_file)
    else:
        print("Не удалось скачать файлы")
        return
    
    if args.use_iterator:
        print("\nДемонстрация итератора:")
        iterator = AudioFileIterator(annotation_file)
        print(f"Файлов в итераторе: {len(iterator)}")
        
        print("Первые 5 файлов:")
        for i, file_path in enumerate(iterator, 1):
            file_obj = Path(file_path)
            duration = downloader.get_audio_duration_from_file(file_obj)
            size_mb = file_obj.stat().st_size / (1024 * 1024)
            print(f"  {i}. {file_obj.name} ({duration:.1f} сек, {size_mb:.2f} MB)")
            if i >= 5:
                break

if __name__ == "__main__":
    main()