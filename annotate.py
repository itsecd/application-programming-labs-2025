# annotate.py
import os
import csv

def give_abs_rel_path(dir_img: str) -> list[dict[str, str]]:
    """
    Получение абсолютных и относительных путей скачанных изображений
    :param dir_img: путь к основной папке с изображениями
    :return: абсолютный и относительный путь для каждого изображения
    """
    # Абсолютный путь к корневой папке данных
    absolute_data_dir = os.path.abspath(dir_img)

    data_path = []

    # Рекурсивно обходим все подпапки
    for root, _, files in os.walk(absolute_data_dir):
        for file in files:
            # Полный абсолютный путь к файлу
            absolute_path = os.path.join(root, file)


            # Относительный путь
            relative_path = os.path.relpath(absolute_path, absolute_data_dir)

            data_path.append({'absolute_path': absolute_path, 'relative_path': relative_path})

    if not data_path:
        return []

    return data_path


def create_annotation(dir_annot_file: str, data_path: list[dict[str, str]], fieldnames: list[str]) -> None:
    """
    Создание аннотации
    :param dir_annot_file: путь к файлу аннотации
    :param data_path: список словарей со значениями абсолютного и относительного путей для каждого изображения
    :param fieldnames: список ключей к значениям словаря
    """
    with open(dir_annot_file, 'w', encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        writer.writerows(data_path)