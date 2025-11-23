import argparse
import cv2
import numpy as np
import os
import sys



def parse_args() -> argparse.Namespace:

    p = argparse.ArgumentParser(description="Сделать изображение полутоновым")

    p.add_argument("-i",
                   "--input",
                   required=True,
                   help="Путь к исходному изображению")

    p.add_argument("-o",
                   "--output",
                   default="Save_Result",
                   help="Путь для сохранения результата")

    return p.parse_args()

def read_image(path: str) -> np.ndarray:

    if not os.path.exists(path):
        print(f"Файл {path} не найден")
        sys.exit(1)

    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)  # возможно 1,3 или 4 канала

    if img is None:
        print(f"Не удалось прочитать изображение с помощью OpenCV: {path}")
        sys.exit(1)

    return img

def print_image_info(img: np.ndarray) -> None:
    shape = img.shape
    print(f"Размер исходного файла: {shape[1]}×{shape[0]}")


def main():
    args = parse_args()

    img = read_image(args.input)

    print_image_info(img)

if __name__ == "__main__":
    main()