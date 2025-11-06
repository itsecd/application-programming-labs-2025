import numpy as np
import matplotlib.pyplot as plt


def show_image(img_rgb: np.ndarray, img_changed: np.ndarray) -> None:
    """
    Отображение изображения
    """
    plt.subplot(1, 2, 1)
    plt.imshow(img_rgb)
    plt.axis("off")
    plt.title("Image original")
    plt.subplot(1, 2, 2)
    plt.imshow(img_changed)
    plt.axis("off")
    plt.title("Image changed")
    plt.show()
