import argparse

import numpy as np
import cv2
import matplotlib.pyplot as plt


def parse_arguments() -> list:
    """
    Парсинг аргументов из командной строки
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--img_path", default="turtle.jpg",  type=str, help="input image path")
    parser.add_argument("-o", "--output_path", default="another_turtle.jpg",  type=str, help="output image path")
    args = parser.parse_args()
    return [args.img_path, args.output_path]


def read_image(input_path) -> np.ndarray:
    """
    Загрузка исходного изображения
    """
    return cv2.imread(input_path)


def image_to_grayscale(img: np.ndarray) -> np.ndarray:
    """
    Делает изображение полутоновым
    """
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def convert_to_rgb(img: np.ndarray) -> np.ndarray:
    """
    Переводит изображение в RGB для работы с matplotlib
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def show_images(img_in: np.ndarray, img_out: np.ndarray) -> None:
    """
    Выводит исходное и конечное изображения на одном "графике"
    """
    fig, ax = plt.subplots(1, 2)
    ax[0].imshow(img_in); ax[0].set_title("Исходное изображение"); ax[0].axis("off")
    ax[1].imshow(img_out); ax[1].set_title("Полученное изображение"); ax[1].axis("off")
    plt.show()


def main() -> None:
    try:
        input_path, output_path = parse_arguments()
        img = convert_to_rgb(read_image(input_path))
        img_gray = convert_to_rgb(image_to_grayscale(img))
        cv2.imwrite(output_path, img_gray)
        shape = img.shape
        print("Высота: ", shape[0], "\nШирина: ", shape[1])
        show_images(img, img_gray)
    except Exception as exc:
        print(f"Возникла ошибка: {exc}")


if __name__ == "__main__":

    main()
