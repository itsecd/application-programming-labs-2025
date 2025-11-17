from __future__ import annotations

import cv2
import matplotlib.pyplot as plt
import numpy as np

from io_utils import image_size


def bgr_to_rgb(img_bgr: np.ndarray) -> np.ndarray:
    """Преобразует BGR в RGB."""
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)


def print_sizes(img1: np.ndarray, img2: np.ndarray) -> None:
    """Печатает размеры двух изображений."""
    w1, h1 = image_size(img1)
    w2, h2 = image_size(img2)
    print(f"Image1: width={w1}, height={h1}")
    print(f"Image2: width={w2}, height={h2}")


def show_images(
    img1_bgr: np.ndarray,
    img2_bgr: np.ndarray,
    result_bgr: np.ndarray,
) -> None:
    """Показывает исходные изображения и результат."""
    plt.imshow(bgr_to_rgb(img1_bgr))
    plt.title("Image 1 (base)")
    plt.axis("off")
    plt.show()

    plt.imshow(bgr_to_rgb(img2_bgr))
    plt.title("Image 2 (overlay)")
    plt.axis("off")
    plt.show()

    plt.imshow(bgr_to_rgb(result_bgr))
    plt.title("Result (alpha blend)")
    plt.axis("off")
    plt.show()