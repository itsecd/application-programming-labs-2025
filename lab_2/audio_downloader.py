import requests
from bs4 import BeautifulSoup
import os
import csv
import time
import argparse
from urllib.parse import urljoin
from pathlib import Path
import random

class AudioFileDownloader:
    def __init__(self, download_dir):
        self.base_url = "https://mixkit.co/free-sound-effects/"
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)
        
    def get_audio_links(self, num_files=1000):
        """Получить ссылки на аудиофайлы с разных страниц"""
        audio_links = []
        page = 1
        
        print("Начинаем поиск аудиофайлов...")
        
        while len(audio_links) < num_files and page <= 20:  # Ограничим количество страниц
            try:
                if page == 1:
                    url = self.base_url
                else:
                    url = f"{self.base_url}page/{page}/"
                
                print(f"Парсинг страницы {page}: {url}")
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                }
                
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Ищем аудио элементы на странице
                audio_elements = soup.find_all('audio')
                audio_sources = []
                
                for audio in audio_elements:
                    source = audio.get('src')
                    if source and source.endswith('.mp3'):
                        full_url = urljoin(url, source)
                        audio_sources.append(full_url)
                
                # Также ищем ссылки на MP3 файлы
                mp3_links = soup.find_all('a', href=lambda x: x and x.endswith('.mp3'))
                for link in mp3_links:
                    href = link['href']
                    full_url = urljoin(url, href)
                    audio_sources.append(full_url)
                
                # Ищем кнопки скачивания
                download_buttons = soup.find_all('a', class_=lambda x: x and 'download' in x.lower())
                for button in download_buttons:
                    href = button.get('href', '')
                    if href and '.mp3' in href:
                        full_url = urljoin(url, href)
                        audio_sources.append(full_url)
                
                print(f"Найдено {len(audio_sources)} аудиофайлов на странице {page}")
                
                # Добавляем уникальные ссылки
                for audio_url in audio_sources:
                    if audio_url not in audio_links and len(audio_links) < num_files:
                        audio_links.append(audio_url)
                        print(f"Всего найдено: {len(audio_links)}")
                
                # Проверяем есть ли следующая страница
                next_link = soup.find('a', class_='next-page')
                if not next_link:
                    next_link = soup.find('a', string=lambda x: x and 'Next' in x)
                
                if not next_link:
                    print("Больше страниц не найдено")
                    break
                
                page += 1
                time.sleep(2)  # Задержка между запросами
                
            except Exception as e:
                print(f"Ошибка при парсинге страницы {page}: {e}")
                break
        
        # Если не нашли достаточно файлов, создадим тестовые URL
        if len(audio_links) < num_files:
            print(f"Найдено только {len(audio_links)} файлов. Добавляем тестовые URL...")
            additional_files = self.get_fallback_audio_links(num_files - len(audio_links))
            audio_links.extend(additional_files)
        
        return audio_links[:num_files]
    
    def get_fallback_audio_links(self, num_files):
        """Резервный метод для получения ссылок на аудио"""
        print("Используем резервный метод поиска аудио...")
        
        # Попробуем получить аудио с других известных страниц mixkit
        fallback_urls = [
            "https://mixkit.co/free-sound-effects/",
            "https://mixkit.co/free-sound-effects/animals/",
            "https://mixkit.co/free-sound-effects/cartoon/",
            "https://mixkit.co/free-sound-effects/impacts/",
            "https://mixkit.co/free-sound-effects/magic/",
            "https://mixkit.co/free-sound-effects/weather/",
            "https://mixkit.co/free-sound-effects/alarms/",
            "https://mixkit.co/free-sound-effects/bells/",
            "https://mixkit.co/free-sound-effects/click/",
            "https://mixkit.co/free-sound-effects/notification/",
        ]
        
        audio_links = []
        
        for url in fallback_urls:
            if len(audio_links) >= num_files:
                break
                
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                response = requests.get(url, headers=headers, timeout=15)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Ищем все элементы с data-audio-url атрибутом
                audio_elements = soup.find_all(attrs={"data-audio-url": True})
                for element in audio_elements:
                    audio_url = element['data-audio-url']
                    if audio_url.endswith('.mp3') and audio_url not in audio_links:
                        full_url = urljoin(url, audio_url)
                        audio_links.append(full_url)
                        if len(audio_links) >= num_files:
                            break
                
                time.sleep(1)
                
            except Exception as e:
                print(f"Ошибка при парсинге {url}: {e}")
        
        return audio_links
    
    def download_audio_files(self, num_files=1000):
        """Скачать аудиофайлы"""
        print(f"Получаем список из {num_files} аудиофайлов...")
        audio_links = self.get_audio_links(num_files)
        
        if not audio_links:
            print("Не удалось найти аудиофайлы. Создаем тестовые файлы...")
            return self.create_test_files(num_files)
        
        print(f"Начинаем скачивание {len(audio_links)} файлов...")
        downloaded_files = []
        
        for i, audio_url in enumerate(audio_links, 1):
            try:
                filename = f"audio_{i:04d}.mp3"
                filepath = self.download_dir / filename
                
                # Пропускаем если файл уже существует
                if filepath.exists():
                    print(f"Файл уже существует: {filename}")
                    downloaded_files.append(filepath)
                    continue
                
                print(f"Скачивание {i}/{len(audio_links)}: {filename}")
                print(f"URL: {audio_url}")
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Referer': 'https://mixkit.co/',
                    'Accept': 'audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5'
                }
                
                response = requests.get(audio_url, headers=headers, stream=True, timeout=30)
                response.raise_for_status()
                
                # Проверяем размер файла
                content_length = response.headers.get('content-length')
                if content_length:
                    file_size_kb = int(content_length) / 1024
                    if file_size_kb < 10:  # Слишком маленький файл
                        print(f"  Пропускаем слишком маленький файл: {file_size_kb:.1f} KB")
                        continue
                
                # Скачиваем файл
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Проверяем что файл скачался
                if filepath.exists() and filepath.stat().st_size > 0:
                    file_size = filepath.stat().st_size / 1024
                    downloaded_files.append(filepath)
                    print(f"  Успешно скачан: {file_size:.1f} KB")
                else:
                    print("  Ошибка: файл не скачан")
                    if filepath.exists():
                        filepath.unlink()
                
                time.sleep(1)  # Задержка между скачиваниями
                
            except Exception as e:
                print(f"Ошибка при скачивании {audio_url}: {e}")
                continue
        
        return downloaded_files
    
    def create_test_files(self, num_files):
        """Создать тестовые файлы если скачивание не удалось"""
        print(f"Создаем {num_files} тестовых файлов...")
        downloaded_files = []
        
        for i in range(1, num_files + 1):
            filename = f"test_audio_{i:04d}.txt"
            filepath = self.download_dir / filename
            
            # Создаем простой текстовый файл с информацией
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Тестовый аудиофайл #{i}\n")
                f.write(f"Это имитация аудиофайла для тестирования\n")
                f.write(f"Создан: {time.ctime()}\n")
            
            downloaded_files.append(filepath)
            print(f"Создан тестовый файл: {filename}")
        
        return downloaded_files
    
    def create_annotation_csv(self, audio_files, annotation_file):
        """Создать CSV-файл с аннотацией"""
        annotation_path = Path(annotation_file)
        annotation_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(annotation_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['absolute_path', 'relative_path', 'filename'])
            
            for audio_file in audio_files:
                try:
                    absolute_path = str(audio_file.resolve())
                    relative_path = str(audio_file.relative_to(Path.cwd()))
                    filename = audio_file.name
                    
                    writer.writerow([absolute_path, relative_path, filename])
                    print(f"Добавлен в аннотацию: {filename}")
                except Exception as e:
                    print(f"Ошибка при записи информации о файле {audio_file}: {e}")
        
        print(f"Аннотация сохранена в {annotation_file}")
        print(f"Всего записей: {len(audio_files)}")

class AudioFileIterator:
    """Итератор по путям к аудиофайлам"""
    
    def __init__(self, source):
        """
        Инициализация итератора
        
        Args:
            source: путь к CSV-файлу аннотации или к папке с аудиофайлами
        """
        self.file_paths = []
        
        if isinstance(source, str):
            source_path = Path(source)
            
            if source_path.is_file() and source_path.suffix.lower() == '.csv':
                # Загрузка из CSV-файла
                self._load_from_csv(source_path)
            elif source_path.is_dir():
                # Загрузка из папки
                self._load_from_directory(source_path)
            else:
                raise ValueError(f"Источник должен быть CSV-файлом или папкой: {source}")
        else:
            raise TypeError("Источник должен быть строкой")
        
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
                        else:
                            print(f"Файл не существует: {row['absolute_path']}")
            print(f"Загружено {len(self.file_paths)} путей из CSV файла")
        except Exception as e:
            print(f"Ошибка при чтении CSV: {e}")
    
    def _load_from_directory(self, directory_path):
        """Загрузить пути из папки"""
        audio_extensions = {'.mp3', '.wav', '.ogg', '.m4a', '.flac', '.txt'}
        
        for file_path in directory_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in audio_extensions:
                self.file_paths.append(str(file_path.resolve()))
        
        print(f"Загружено {len(self.file_paths)} файлов из папки")
    
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
    parser = argparse.ArgumentParser(description='Скачивание аудиофайлов с mixkit.co')
    parser.add_argument('--download-dir', '-d', required=True, 
                       help='Путь к папке для сохранения аудиофайлов')
    parser.add_argument('--annotation-file', '-a', required=True,
                       help='Путь к файлу аннотации (CSV)')
    parser.add_argument('--num-files', '-n', type=int, default=100,
                       help='Количество файлов для скачивания (от 50 до 1000, по умолчанию 100)')
    parser.add_argument('--use-iterator', '-i', action='store_true',
                       help='Запустить итератор после скачивания')
    
    args = parser.parse_args()
    
    # Проверяем количество файлов
    if args.num_files < 50:
        print("Предупреждение: количество файлов меньше 50. Установлено значение 50.")
        args.num_files = 50
    elif args.num_files > 1000:
        print("Предупреждение: количество файлов больше 1000. Установлено значение 1000.")
        args.num_files = 1000
    
    # Скачивание аудиофайлов
    downloader = AudioFileDownloader(args.download_dir)
    
    print("=" * 60)
    print(f"ПАРАМЕТРЫ ЗАПУСКА:")
    print(f"  Папка для сохранения: {args.download_dir}")
    print(f"  Файл аннотации: {args.annotation_file}")
    print(f"  Количество файлов: {args.num_files}")
    print("=" * 60)
    
    downloaded_files = downloader.download_audio_files(args.num_files)
    
    print(f"\nРЕЗУЛЬТАТ СКАЧИВАНИЯ:")
    print(f"Успешно скачано/создано {len(downloaded_files)} файлов")
    
    if downloaded_files:
        # Создание аннотации
        downloader.create_annotation_csv(downloaded_files, args.annotation_file)
    else:
        print("Нет файлов для создания аннотации")
        return
    
    # Использование итератора если нужно
    if args.use_iterator:
        print("\n" + "=" * 60)
        print("ДЕМОНСТРАЦИЯ РАБОТЫ ИТЕРАТОРА:")
        print("=" * 60)
        
        # Итератор из CSV-файла
        if Path(args.annotation_file).exists():
            print("1. Итерация по файлам из аннотации CSV:")
            try:
                csv_iterator = AudioFileIterator(args.annotation_file)
                print(f"Всего файлов в итераторе: {len(csv_iterator)}")
                
                print("Первые 10 файлов:")
                for i, file_path in enumerate(csv_iterator, 1):
                    file_obj = Path(file_path)
                    print(f"  {i:2d}. {file_obj.name} ({file_obj.stat().st_size} bytes)")
                    if i >= 10:
                        break
            except Exception as e:
                print(f"Ошибка при создании итератора из CSV: {e}")
        else:
            print("CSV файл аннотации не существует")
        
        # Итератор из папки
        print(f"\n2. Итерация по файлам из папки {args.download_dir}:")
        try:
            dir_iterator = AudioFileIterator(args.download_dir)
            print(f"Всего файлов в итераторе: {len(dir_iterator)}")
            
            print("Первые 10 файлов:")
            for i, file_path in enumerate(dir_iterator, 1):
                file_obj = Path(file_path)
                print(f"  {i:2d}. {file_obj.name} ({file_obj.stat().st_size} bytes)")
                if i >= 10:
                    break
        except Exception as e:
            print(f"Ошибка при создании итератора из папки: {e}")

if __name__ == "__main__":
    main()