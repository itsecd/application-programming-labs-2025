import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def args_parse() -> argparse.Namespace:
    """Данная функция получает аргументы(input_file_path, result_file_path)"""
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input_file", help="Путь к исходноому изображению")
    parser.add_argument("-r", "--result_file", help="Путь для сохранения обработанного изображения")

    args = parser.parse_args()

    
    if (args.input_file and args.result_file) is not None:
        return args
    else:
        raise Exception("Incorrectly passed arguments")


def get_img_size(img: cv2.typing.MatLike) -> tuple[int, int, int]:
    """Данная функция возвращает размеры изображения"""
    return img.shape


def make_halftone_img(img: cv2.typing.MatLike) -> cv2.typing.MatLike:
    """Данная функция делает изображение формата BGR полутоновым.
       Возвращает полутоновое изображение в формате RGB"""
    new_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(new_img, cv2.COLOR_GRAY2RGB)


def save_img(path: str, img: cv2.typing.MatLike) -> None:
    """Функция сохранения обработанного изображения"""
    result_path = os.path.dirname(path)
    
    if not os.path.exists(result_path):
        os.makedirs(result_path, exist_ok=True)
    
    cv2.imwrite(path, img)


def show_images(img1: cv2.typing.MatLike, img2: cv2.typing.MatLike) -> None:
    """Данная функция демонстрирует два изображения"""
    plt.figure(1)
    plt.title("Исходное изображение")
    plt.axis("off")
    plt.imshow(img1)
    
    plt.figure(2)
    plt.title("Обработанное изображение")
    plt.axis("off")
    plt.imshow(img2)
    
    plt.show()


def main() -> None:
    arguments = args_parse()
    input_file = arguments.input_file
    result_file = arguments.result_file

    img_brg = cv2.imread(input_file)
    
    if img_brg is None:
        raise FileNotFoundError("Can't find image")
    
    img_rgb = cv2.cvtColor(img_brg, cv2.COLOR_BGR2RGB)

    height, width, channels = get_img_size(img_rgb)
    print("Размеры изображения:", 
          f" Высота: {height}",
          f" Ширина: {width}",
          f" Каналы изображения: {channels}", sep="\n")
    
    img_gray = make_halftone_img(img_brg)
    
    show_images(img_rgb, img_gray)
    save_img(result_file, img_gray)


if __name__ == "__main__":
    main()