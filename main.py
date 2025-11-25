# main.py
import argparse
import sys

from annotate import give_abs_rel_path, create_annotation
from download import download_images
from file_iterator import FileIterator

# Список доступных цветов
list_of_colors = ["red", "green", "blue", "purple"]

def main():
    parser = argparse.ArgumentParser()

    # Аргументы для путей
    parser.add_argument("-d",
                        "--directory_img",
                        default = "turtle_images",
                        help = "Путь к папке для сохранения изображений")
    parser.add_argument("-c",
                        "--colors",
                        nargs='+',
                        required=True,
                        choices=list_of_colors,
                        help="Цвета черепахи")

    parser.add_argument("-a",
                        "--annotation_file",
                        default="annotation.csv",
                        help="Путь к файлу аннотации CSV")

    args = parser.parse_args()

    # Количество изображений для скачивания
    count = 50

    # Скачивание изображений
    print("\nСкачивание")
    download_images(args.directory_img, args.colors, count)

    # Создание аннотации
    print("\nСоздание Аннотации")

    data_path = give_abs_rel_path(args.directory_img)
    headers = ["absolute_path", "relative_path"]
    create_annotation(args.annotation_file, data_path, headers)

    print("\nАннотация создана")

    #Демонстрация работы итератора
    iterator = FileIterator(args.annotation_file)
    for i in iterator:
        print(i)

if __name__ == '__main__':
    main()