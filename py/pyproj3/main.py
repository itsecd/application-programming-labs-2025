import argparse

import cv2
import numpy
import matplotlib.pyplot as plt


def show_image(image: numpy.ndarray) -> None:
    """
    ввыводим изображение при помощи matplotlib
    """
    plt.imshow(image)
    plt.axis('off')
    plt.show()


def change_size(image: numpy.ndarray, new_size: tuple[int, int]) -> numpy.ndarray:
    """
    изменяем ширину и высоту изображения
    """
    return cv2.resize(
        image,
        new_size,
        interpolation=cv2.INTER_LINEAR
    )


def print_size(image: numpy.ndarray) -> None:
    """
    выводим ширину и высоту изображения
    """
    size = image.shape
    print(f"ширина = {size[1]}, высота = {size[0]}")


def size_format(size: str) -> tuple[int, int]:
    """
    приводим строчное обозначение размера в формат кортежа
    """
    size = size.split('X')
    if len(size) != 2:
        raise ValueError('размер изображения должен быть в формате widthXheight')
    width = int(size[0])
    height = int(size[1])
    return width, height

def main():
    try:

        parser = argparse.ArgumentParser(description="Преобразовывает изображение на пути path_in в размер size и сохраняет его по path_out")

        parser.add_argument("path_in", type=str, help="абсолютный путь до файла исходного изображения")
        parser.add_argument("path_out", type=str, help="путь для установки измененого изображения")
        parser.add_argument("size", type=str, help="размер нового изображения формата widthXheight")

        args = parser.parse_args()

        size = size_format(args.size)

        image = cv2.imread(args.path_in)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        print_size(image)

        show_image(image)

        resized_image = change_size(image, size)

        show_image(resized_image)

        cv2.imwrite(args.path_out, resized_image)

    except cv2.error as e:
        print(e)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()