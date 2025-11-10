import csv
from config import HEADERS
import os
import re
import requests
from typing import List, Dict


def good_filename(name: str) -> str:
    """
    Создает безопасное имя файла из произвольной строки.
    """
    name = re.sub(r'[^a-zA-Z0-9а-яА-ЯёЁ_.-]+', "_", name)
    name = re.sub(r'_+', "_", name)
    name = name.strip("_")
    return name[:100]


def download_sounds(sounds: List[Dict[str, str]],
                    dest_dir: str) -> List[Dict[str, str]]:
    """
    Скачивает звуки и возвращает список скачанных файлов.
    """
    os.makedirs(dest_dir, exist_ok=True)
    downloaded_files = []

    for i, sound in enumerate(sounds, start=1):
        safe_name = good_filename(sound["title"])
        filename = f"{i:03d}_{safe_name}.mp3"
        file_path = os.path.join(dest_dir, filename)

        try:
            resp = requests.get(sound["mp3_link"], headers=HEADERS, timeout=30)
            resp.raise_for_status()

            if len(resp.content) < 1024:
                continue

            with open(file_path, "wb") as f:
                f.write(resp.content)

            downloaded_files.append({
                "title": sound["title"],
                "file_path": file_path
            })

        except Exception:
            continue

    return downloaded_files


def create_annotation(downloaded_files: List[Dict[str, str]],
                      csv_path: str) -> None:
    """
    Создает CSV файл аннотации.
    """
    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=[
            "title", "absolute_path", "relative_path"])
        writer.writeheader()

        for file_info in downloaded_files:
            abs_path = os.path.abspath(file_info["file_path"])
            rel_path = os.path.relpath(file_info["file_path"],
                                       start=os.path.dirname(csv_path))

            writer.writerow({
                "title": file_info["title"],
                "absolute_path": abs_path,
                "relative_path": rel_path
            })
