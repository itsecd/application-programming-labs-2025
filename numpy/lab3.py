#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import cv2
import argparse
import sys


def image_handler(path: str):
    img_bgr = cv2.imread(path)
    if img_bgr is None:
        raise FileNotFoundError(f"Не удалось открыть изображение по пути: {path}")

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    negative_rgb = 255 - img_rgb

    return img_rgb, negative_rgb, img_rgb.shape


def display_images(images: list[np.ndarray]) -> None:
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.title('Исходное изображение')
    plt.imshow(images[0])
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title('Обработанное изображение')
    plt.imshow(images[1])
    plt.axis('off')

    plt.show()


def args_parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Инверсия цветов изображения.")
    parser.add_argument("--input", required=True, help="Путь к исходному изображению.")
    parser.add_argument("--output", required=True, help="Путь к обработанному изображению.")
    return parser.parse_args()


def main():
    args = args_parse()

    img_rgb, negative_rgb, shape = image_handler(args.input)
    print("Shape:", shape)

    negative_bgr = cv2.cvtColor(negative_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite(args.output, negative_bgr)

    display_images([img_rgb, negative_rgb])


if __name__ == "__main__":
    main()
