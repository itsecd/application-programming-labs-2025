import cv2
import numpy as np
import matplotlib.pyplot as plt


def show_image(original: np.ndarray, transformed: np.ndarray) -> None:
    """
    отображает исходное и преобразованное изображение рядом
    """
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].imshow(original)
    axs[0].set_title("Исходное")
    axs[0].axis("off")

    axs[1].imshow(transformed)
    axs[1].set_title("Преобразованное")
    axs[1].axis("off")

    plt.tight_layout()
    plt.show()


def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
    """
    поворачивает изображение на заданный угол
    """
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    rot_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    rotated = cv2.warpAffine(image, rot_matrix, (w, h))

    return rotated
