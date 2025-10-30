import argparse

import numpy as np

from display_comparison import display_comparison
from add_white_noise import add_white_noise
from load_images import load_images
from save_noisy_images import save_noisy_images


def parse_arguments() -> argparse.Namespace:
    """ "
    функция для парсинга путей
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=str, help="путь к файлу с фото")
    parser.add_argument("input_dir", type=str, help="путь к файлу сохранения фото")
    args = parser.parse_args()
    return args


def print_image_sizes(images: list[np.ndarray]) -> None:
    """
    функция для вывода размера изображение
    """
    print("Размер каждого изображения")
    i = 1
    for img in images:
        print(i, "-", img.shape)
        i = i + 1


def main() -> None:
    args = parse_arguments()
    images = load_images(args.input_dir)
    print_image_sizes(images)
    noisy_images = add_white_noise(images)
    print()
    display_comparison(noisy_images, images)
    save_noisy_images(noisy_images, args.output_dir)


if __name__ == "__main__":
    main()
