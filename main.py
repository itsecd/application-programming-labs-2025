# main.py
import argparse
import sys

from download import download_images


# Список доступных цветов
list_of_colors = ["red", "green", "blue", "purple"]

def main():
    parser = argparse.ArgumentParser()

    # Аргументы для путей
    parser.add_argument("-d",
                        "--directory_img",
                        default = "turtle_images",
                        help = "Путь к папке для сохранения изображений")

    parser.add_argument("-a",
                        "--annotation_file",
                        default = "annotation.csv",
                        help = "Путь к файлу аннотации CSV")

    args = parser.parse_args()

    # Ввод цветов для черепахи
    print(f"\nДоступные цвета для черепахи: {list_of_colors}")
    colors = input("Перечислите нужные цвета чрез пробел (без других разделителей): ")
    colors = colors.lower()
    colors = colors.split(" ")
    result_list_colors = []
    for color in colors:
        if color in list_of_colors:
            result_list_colors.append(color)

    if len(result_list_colors) == 0:
        print("Ошибка: Ни один из ведённых вами цветов не доступен для черепахи")
        sys.exit(1)

    #Количество изображений для скачивания
    count = 50

    #Скачивание изображений
    print("\nСкачивание")
    download_images(args.directory_img, result_list_colors, count)

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