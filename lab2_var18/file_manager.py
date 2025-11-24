"""Модуль для работы с файлами и создания аннотаций."""
import csv
import os
import re
import requests
from typing import List, Dict
from settings import REQUEST_HEADERS


def create_safe_filename(original_name: str) -> str:
    """
    Создает безопасное имя файла из произвольной строки.

    Args:
        original_name: Исходное имя файла

    Returns:
        Безопасное имя файла
    """
    try:
        safe_name = re.sub(r'[^a-zA-Z0-9а-яА-ЯёЁ_.-]+', "_", original_name)
        safe_name = re.sub(r'_+', "_", safe_name)
        safe_name = safe_name.strip("_")
        return safe_name[:100]
    except Exception as e:
        print(f"Ошибка при создании имени файла: {e}")
        return "unknown_sound"


def download_human_sounds(
    sounds_data: List[Dict[str, str]],
    target_directory: str
) -> List[Dict[str, str]]:
    """
    Скачивает звуки людей в указанную директорию.

    Args:
        sounds_data: Данные о звуках для скачивания
        target_directory: Целевая директория

    Returns:
        Список информации о скачанных файлах
    """
    try:
        os.makedirs(target_directory, exist_ok=True)
        downloaded_files = []

        for index, sound in enumerate(sounds_data, start=1):
            filename_base = create_safe_filename(sound["name"])
            full_filename = f"{index:03d}_{filename_base}.mp3"
            complete_path = os.path.join(target_directory, full_filename)

            try:
                response = requests.get(
                    sound["audio_url"],
                    headers=REQUEST_HEADERS,
                    timeout=30
                )
                response.raise_for_status()

                if len(response.content) < 1024:
                    continue

                with open(complete_path, "wb") as file:
                    file.write(response.content)

                downloaded_files.append({
                    "name": sound["name"],
                    "file_location": complete_path
                })

            except Exception as e:
                print(f"Ошибка при скачивании {sound['name']}: {e}")
                continue

        return downloaded_files
    except Exception as e:
        print(f"Ошибка при скачивании звуков: {e}")
        return []


def create_sounds_annotation(
    downloaded_files: List[Dict[str, str]],
    annotation_path: str
) -> None:
    """
    Создает CSV файл аннотации для скачанных звуков.

    Args:
        downloaded_files: Список информации о скачанных файлах
        annotation_path: Путь к файлу аннотации
    """
    try:
        with open(annotation_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=["name", "absolute_path", "relative_path"]
            )
            writer.writeheader()

            for file_data in downloaded_files:
                absolute_path = os.path.abspath(file_data["file_location"])
                relative_path = os.path.relpath(
                    file_data["file_location"],
                    start=os.path.dirname(annotation_path)
                )

                writer.writerow({
                    "name": file_data["name"],
                    "absolute_path": absolute_path,
                    "relative_path": relative_path
                })
    except Exception as e:
        print(f"Ошибка при создании аннотации: {e}")