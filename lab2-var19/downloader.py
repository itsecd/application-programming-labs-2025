import os
import requests
from bs4 import BeautifulSoup
from typing import List, Tuple
from urllib.parse import urljoin
import time
from utils import ensure_directory, create_annotation_file


class SoundDownloader:
    """
    Класс для скачивания звуковых файлов с сайта mixkit.co
    """

    def __init__(self, base_url: str = "https://mixkit.co") -> None:
        """
        Инициализация загрузчика

        Args:
            base_url: Базовый URL сайта
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_animal_sounds_links(self, max_count: int = 50) -> List[str]:
        """
        Получает ссылки на звуки животных

        Args:
            max_count: Максимальное количество звуков для скачивания

        Returns:
            Список URL звуковых файлов
        """
        sound_links = []
        page = 1

        try:
            while len(sound_links) < max_count:
                url = f"{self.base_url}/free-sound-effects/animals/?page={page}"
                print(f"Парсинг страницы: {url}")

                response = self.session.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                # Находим все аудио элементы
                audio_elements = soup.find_all('audio')

                if not audio_elements:
                    print("Больше звуков не найдено")
                    break

                for audio in audio_elements:
                    source = audio.find('source')
                    if source and source.get('src'):
                        sound_url = urljoin(self.base_url, source['src'])
                        sound_links.append(sound_url)

                        if len(sound_links) >= max_count:
                            break

                page += 1
                time.sleep(1)  # Задержка между запросами

        except Exception as e:
            print(f"Ошибка при парсинге страниц: {e}")

        return sound_links[:max_count]

    def download_sounds(self, download_dir: str, annotation_file: str, max_count: int = 50) -> None:
        """
        Скачивает звуковые файлы и создает аннотацию

        Args:
            download_dir: Директория для сохранения
            annotation_file: Путь к файлу аннотации
            max_count: Максимальное количество файлов для скачивания
        """
        try:
            ensure_directory(download_dir)

            print("Поиск ссылок на звуки животных...")
            sound_links = self.get_animal_sounds_links(max_count)

            if not sound_links:
                print("Не удалось найти звуки для скачивания")
                return

            print(f"Найдено {len(sound_links)} звуков. Начинаю загрузку...")

            annotation_data = []

            for i, sound_url in enumerate(sound_links, 1):
                try:
                    # Получаем имя файла из URL
                    filename = os.path.basename(sound_url.split('?')[0])
                    if not filename.endswith('.mp3'):
                        filename = f"animal_sound_{i}.mp3"

                    file_path = os.path.join(download_dir, filename)

                    print(f"Скачивание {i}/{len(sound_links)}: {filename}")

                    response = self.session.get(sound_url)
                    response.raise_for_status()

                    # Сохраняем файл
                    with open(file_path, 'wb') as f:
                        f.write(response.content)

                    # Добавляем в аннотацию
                    absolute_path = os.path.abspath(file_path)
                    relative_path = os.path.relpath(file_path)
                    annotation_data.append((absolute_path, relative_path))

                    time.sleep(0.5)  # Задержка между загрузками

                except Exception as e:
                    print(f"Ошибка при скачивании {sound_url}: {e}")
                    continue

            # Создаем файл аннотации
            if annotation_data:
                create_annotation_file(annotation_file, annotation_data)
                print(f"Успешно скачано {len(annotation_data)} звуков")
            else:
                print("Не удалось скачать ни одного звука")

        except Exception as e:
            print(f"Общая ошибка при скачивании: {e}")