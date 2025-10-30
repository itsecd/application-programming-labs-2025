import cv2
import matplotlib.pyplot as plt
import numpy as np


def display_comparison(
    noisy_images: list[np.ndarray], original_images: list[np.ndarray]
) -> None:
    """
    функция для вывода на экран двух картинок, с белым шумом и без
    """
    for original_img, noisy_img in zip(original_images, noisy_images):
        original_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
        noisy_rgb = cv2.cvtColor(noisy_img, cv2.COLOR_BGR2RGB)
        plt.subplot(1, 2, 1)
        plt.imshow(original_rgb)
        plt.axis("off")
        plt.title("Без белого шума")
        plt.subplot(1, 2, 2)
        plt.imshow(noisy_rgb)
        plt.axis("off")
        plt.title("C белым шумом")
        plt.show()
