import requests
from bs4 import BeautifulSoup
import os
import csv
import time
import argparse
from urllib.parse import urljoin
from pathlib import Path
import mutagen
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
import io

class AudioFileDownloader:
    def __init__(self, download_dir):
        self.base_url = "https://mixkit.co/free-sound-effects/"
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)
        
    def get_audio_links(self, num_files=1000):
        """Получить ссылки на аудиофайлы с основной страницы"""
        audio_links = []
        page = 1
        
        print("Поиск аудиофайлов на Mixkit...")
        
        while len(audio_links) < num_files and page <= 50:
            try:
                if page == 1:
                    url = self.base_url
                else:
                    url = f"{self.base_url}?page={page}"
                
                print(f"Парсинг страницы {page}: {url}")
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                }
                
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Ищем все карточки с аудио
                audio_cards = soup.find_all('div', class_=lambda x: x and 'item-grid-card' in x)
                
                if not audio_cards:
                    # Альтернативный поиск карточек
                    audio_cards = soup.find_all('div', class_=lambda x: x and 'card' in x)
                
                print(f"Найдено карточек: {len(audio_cards)}")
                
                for card in audio_cards:
                    if len(audio_links) >= num_files:
                        break
                    
                    # Ищем ссылку на страницу аудио
                    audio_page_link = card.find('a', href=True)
                    if audio_page_link:
                        audio_page_url = urljoin(self.base_url, audio_page_link['href'])
                        
                        # Пропускаем если это не страница конкретного аудио
                        if not self.is_audio_detail_page(audio_page_url):
                            continue
                            
                        direct_audio_url = self.get_direct_audio_url(audio_page_url)
                        
                        if direct_audio_url and direct_audio_url not in audio_links:
                            # Проверяем размер файла перед добавлением
                            if self.check_file_size(direct_audio_url):
                                audio_links.append(direct_audio_url)
                                print(f" Найдено аудио: {len(audio_links)}")
                            else:
                                print("   Файл слишком маленький, пропускаем...")
                    
                    time.sleep(0.2)  # Небольшая задержка
                
                # Проверяем есть ли следующая страница
                next_button = soup.find('a', class_=lambda x: x and 'page-link' in x and 'Next' in str(x))
                if not next_button:
                    next_button = soup.find('a', string=lambda x: x and 'Next' in str(x))
                
                if not next_button:
                    print("Достигнута последняя страница")
                    break
                    
                page += 1
                time.sleep(1)
                
            except Exception as e:
                print(f"Ошибка при парсинге страницы {page}: {e}")
                break
        
        return audio_links[:num_files]
    
    def is_audio_detail_page(self, url):
        """Проверить, что это страница конкретного аудио"""
        return '/free-sound-effects/' in url and url.count('/') >= 5
    
    def check_file_size(self, audio_url, min_size_mb=1.0):
        """Быстрая проверка размера файла"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Range': 'bytes=0-0'
            }
            
            response = requests.head(audio_url, headers=headers, timeout=10)
            content_length = response.headers.get('content-length')
            
            if content_length:
                file_size_mb = int(content_length) / (1024 * 1024)
                # Для MP3: 1MB ≈ 8-10 секунд аудио
                return file_size_mb >= min_size_mb
            
            return True  # Если не удалось проверить, скачиваем
            
        except:
            return True  # Если ошибка, скачиваем файл
    
    def get_direct_audio_url(self, audio_page_url):
        """Получить прямую ссылку на аудиофайл"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(audio_page_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Способ 1: Ищем тег audio
            audio_tag = soup.find('audio')
            if audio_tag:
                src = audio_tag.get('src')
                if src:
                    full_url = urljoin(audio_page_url, src)
                    return full_url
            
            # Способ 2: Ищем ссылки с аудио расширениями
            for ext in ['.mp3', '.wav', '.ogg']:
                audio_links = soup.find_all('a', href=lambda x: x and x.endswith(ext))
                for link in audio_links:
                    href = link['href']
                    full_url = urljoin(audio_page_url, href)
                    return full_url
            
            # Способ 3: Ищем кнопку скачивания
            download_buttons = soup.find_all('button', string=lambda x: x and any(word in str(x).lower() for word in ['download', 'play']))
            for button in download_buttons:
                # Ищем родительскую ссылку
                parent = button.find_parent('a', href=True)
                if parent:
                    href = parent['href']
                    if any(ext in href.lower() for ext in ['.mp3', '.wav', '.ogg']):
                        full_url = urljoin(audio_page_url, href)
                        return full_url
            
            # Способ 4: Ищем в data-атрибутах
            audio_elements = soup.find_all(attrs={"data-url": True})
            for element in audio_elements:
                data_url = element['data-url']
                if any(ext in data_url.lower() for ext in ['.mp3', '.wav', '.ogg']):
                    full_url = urljoin(audio_page_url, data_url)
                    return full_url
                    
        except Exception as e:
            print(f"    Ошибка получения ссылки: {e}")
        
        return None
    
    def download_audio_files(self, num_files=1000):
        """Скачать аудиофайлы с проверкой длительности"""
        print(f"Получаем список из {num_files} аудиофайлов...")
        audio_links = self.get_audio_links(num_files)
        
        if not audio_links:
            print(" Не удалось найти аудиофайлы.")
            return []
        
        print(f"\nНачинаем скачивание {len(audio_links)} файлов...")
        downloaded_files = []
        
        for i, audio_url in enumerate(audio_links, 1):
            try:
                # Определяем расширение
                file_extension = 'mp3'
                for ext in ['.mp3', '.wav', '.ogg']:
                    if ext in audio_url.lower():
                        file_extension = ext[1:]
                        break
                
                filename = f"audio_{i:04d}.{file_extension}"
                filepath = self.download_dir / filename
                
                # Пропускаем существующие файлы с проверкой длительности
                if filepath.exists():
                    duration = self.get_audio_duration_from_file(filepath)
                    if duration and duration >= 10:
                        downloaded_files.append(filepath)
                        print(f"📁 Существующий файл: {filename} ({duration:.1f} сек)")
                        continue
                    else:
                        print(f" Перезаписываем короткий файл: {filename}")
                        filepath.unlink()
                
                print(f"⬇ Скачивание {i}/{len(audio_links)}: {filename}")
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Referer': 'https://mixkit.co/'
                }
                
                # Скачиваем во временный файл
                temp_path = filepath.with_suffix('.tmp')
                
                response = requests.get(audio_url, headers=headers, stream=True, timeout=60)
                response.raise_for_status()
                
                total_size = 0
                with open(temp_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            total_size += len(chunk)
                
                # Проверяем длительность
                duration = self.get_audio_duration_from_file(temp_path)
                file_size_mb = total_size / (1024 * 1024)
                
                if duration and duration >= 10:
                    # Сохраняем файл
                    temp_path.rename(filepath)
                    downloaded_files.append(filepath)
                    print(f"   Успешно: {file_size_mb:.2f} MB, {duration:.1f} сек")
                else:
                    print(f"   Слишком короткий: {duration:.1f} сек, удаляем...")
                    if temp_path.exists():
                        temp_path.unlink()
                
                time.sleep(1)  # Задержка между скачиваниями
                
            except Exception as e:
                print(f" Ошибка скачивания: {e}")
                continue
        
        print(f"\n Результат:")
        print(f" Успешно скачано: {len(downloaded_files)} файлов (>10 сек)")
        
        return downloaded_files
    
    def get_audio_duration_from_file(self, filepath):
        """Получить длительность аудиофайла"""
        try:
            audio = mutagen.File(filepath)
            if audio and hasattr(audio.info, 'length'):
                return audio.info.length
        except Exception as e:
            print(f"    Ошибка определения длительности: {e}")
        return None
    
    def create_annotation_csv(self, audio_files, annotation_file):
        """Создать CSV-файл с аннотацией"""
        annotation_path = Path(annotation_file)
        annotation_path.parent.mkdir(parents=True, exist_ok=True)
        
        valid_files = 0
        
        with open(annotation_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['absolute_path', 'relative_path', 'filename', 'duration_seconds', 'file_size_mb'])
            
            for audio_file in audio_files:
                try:
                    duration = self.get_audio_duration_from_file(audio_file)
                    if duration and duration >= 10:
                        absolute_path = str(audio_file.resolve())
                        relative_path = str(audio_file.relative_to(Path.cwd()))
                        filename = audio_file.name
                        file_size_mb = audio_file.stat().st_size / (1024 * 1024)
                        
                        writer.writerow([absolute_path, relative_path, filename, f"{duration:.1f}", f"{file_size_mb:.2f}"])
                        valid_files += 1
                        print(f" {filename}: {duration:.1f} сек")
                    else:
                        print(f" Удаляем короткий файл из аннотации: {audio_file.name}")
                        if audio_file.exists():
                            audio_file.unlink()
                except Exception as e:
                    print(f"Ошибка обработки файла {audio_file}: {e}")
        
        print(f"\n Аннотация сохранена: {annotation_file}")
        print(f" Файлов в аннотации: {valid_files}")

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
        print(f"Итератор инициализирован с {len(self.file_paths)} файлами")
    
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
        except Exception as e:
            print(f"Ошибка чтения CSV: {e}")
    
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
    parser = argparse.ArgumentParser(description='Скачивание аудиофайлов с Mixkit')
    parser.add_argument('--download-dir', '-d', required=True, 
                       help='Путь к папке для сохранения аудиофайлов')
    parser.add_argument('--annotation-file', '-a', required=True,
                       help='Путь к файлу аннотации (CSV)')
    parser.add_argument('--num-files', '-n', type=int, default=100,
                       help='Количество файлов для скачивания')
    parser.add_argument('--use-iterator', '-i', action='store_true',
                       help='Запустить итератор после скачивания')
    
    args = parser.parse_args()
    
    downloader = AudioFileDownloader(args.download_dir)
    
    print("=" * 60)
    print(" СКАЧИВАНИЕ АУДИОФАЙЛОВ С MIXKIT")
    print(f" Папка: {args.download_dir}")
    print(f" Аннотация: {args.annotation_file}")
    print(f" Количество: {args.num_files} файлов")
    print(f"⏱ Минимальная длительность: 10 секунд")
    print("=" * 60)
    
    downloaded_files = downloader.download_audio_files(args.num_files)
    
    if downloaded_files:
        downloader.create_annotation_csv(downloaded_files, args.annotation_file)
    else:
        print(" Не удалось скачать файлы")
        return
    
    if args.use_iterator:
        print("\n" + "=" * 60)
        print(" ДЕМОНСТРАЦИЯ ИТЕРАТОРА")
        print("=" * 60)
        
        if Path(args.annotation_file).exists():
            iterator = AudioFileIterator(args.annotation_file)
            print(f"Файлов в итераторе: {len(iterator)}")
            
            print("Первые 5 файлов:")
            for i, file_path in enumerate(iterator, 1):
                file_obj = Path(file_path)
                duration = downloader.get_audio_duration_from_file(file_obj)
                size_mb = file_obj.stat().st_size / (1024 * 1024)
                print(f"  {i}. {file_obj.name}")
                print(f"     ⏱ {duration:.1f} сек |  {size_mb:.2f} MB")
                if i >= 5:
                    break

if __name__ == "__main__":
    main()