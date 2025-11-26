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


def get_img_size(img: np.ndarray) -> tuple:
    """Данная функция возвращает размеры изображения"""
    return img.shape


def make_halftone_img(img: np.ndarray) -> np.ndarray:
    """Данная функция делает изображение формата RGB полутоновым.
       Возвращает полутоновое изображение в формате RGB"""
    new_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return cv2.cvtColor(new_img, cv2.COLOR_GRAY2RGB)


def save_img(path: str, img: np.ndarray) -> None:
    """Функция сохранения обработанного изображения"""
    result_path = os.path.dirname(path)
    
    if not os.path.exists(result_path):
        os.makedirs(result_path, exist_ok=True)
    
    cv2.imwrite(path, img)


def show_images(img1: np.ndarray, img2: np.ndarray) -> None:
    """Данная функция выводит два изображения"""
    plt.figure(1)
    plt.title("Исходное изображение")
    plt.axis("off")
    plt.imshow(img1)
    
    plt.figure(2)
    plt.title("Обработанное изображение")
    plt.axis("off")
    plt.imshow(img2)
    
    plt.show()


def image_handler(path: str) -> np.ndarray:
    """Обработка изображения"""
    img_brg = cv2.imread(path)

    if img_brg is None:
        raise FileNotFoundError("Can't find image")

    return cv2.cvtColor(img_brg, cv2.COLOR_BGR2RGB)


def main() -> None:
    arguments = args_parse()
    input_file = arguments.input_file
    result_file = arguments.result_file

    img = image_handler(input_file)
    height, width = get_img_size(img)[0:2]
    print(f"Размеры изображения: {width}x{height}")
    
    img_gray = make_halftone_img(img)
    
    show_images(img, img_gray)
    save_img(result_file, img_gray)


if __name__ == "__main__":
    main()