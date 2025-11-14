import os
import requests
from pathlib import Path


def download_images(keyword: str, date_from: str, date_to: str, max_num: int, save_dir: str) -> None:
    """Создает тестовые файлы изображений"""
    os.makedirs(save_dir, exist_ok=True)

    print(f"Создание изображений '{keyword}'")
    print(f"Период: {date_from} - {date_to}")
    print(f"Целевое количество: {max_num} файлов")

    # Создаем тестовые файлы
    for i in range(max_num):
        filename = f"{keyword}_{i + 1:03d}.jpg"
        filepath = os.path.join(save_dir, filename)

        # Создаем файл
        with open(filepath, 'w') as f:
            f.write(f"Тестовое изображение {keyword} #{i + 1}")

        if (i + 1) % 10 == 0:
            print(f"Создано {i + 1}/{max_num} файлов")

    print(f"Готово! Создано {max_num} файлов в папке '{save_dir}'")