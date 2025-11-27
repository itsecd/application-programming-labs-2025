import cv2
import matplotlib.pyplot as plt
import numpy as np


def to_grayscale(img: np.ndarray) -> np.ndarray:
    """
    Возвращает изображение в полутоновом виде (2D, dtype uint8)
    :param img: многомерный массив пикселей исходного изображения
    :return: многомерный массив пикселей полутонового изображения
    """
    # Если уже single-channel — привести к uint8 и вернуть
    if img.ndim == 2:
        if img.dtype != np.uint8:
            if np.issubdtype(img.dtype, np.floating):
                gray = np.clip(img * 255, 0, 255).astype(np.uint8)
                return gray
            else:
                gray = img.astype(np.uint8)
                return gray
        return img.copy()

    # OpenCV хранит BGR
    shape = img.shape
    # отделим альфа, если есть
    if shape[2] == 4:
        bgr = img[:, :, :3]
    else:
        bgr = img
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    return gray


def show_pair(original: np.ndarray, gray: np.ndarray) -> None:
    """
    Демонстрация исходного изображения и результата
    :param original: многомерный массив пикселей исходного изображения
    :param gray: многомерный массив пикселей полутонового изображения
    """
    # matplotlib ожидает RGB для цветных изображений, и 2D для grayscale
    plt.figure()

    # исходное: если 3- или 4-канальное — конвертируем BGR->RGB
    plt.subplot(1, 2, 1)
    if original.ndim == 2:
        plt.imshow(original, cmap="gray")
    else:
        # BGR -> RGB
        if original.shape[2] == 4:
            bgr = original[:, :, :3]
        else:
            bgr = original
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        plt.imshow(rgb)


    plt.title("Исходное")
    plt.axis("off")

    # результат (gray) — 2D
    plt.subplot(1, 2, 2)
    plt.imshow(gray, cmap="gray")
    plt.title("Полутоновое")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

