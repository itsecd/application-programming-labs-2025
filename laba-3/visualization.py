import matplotlib.pyplot as plt
import cv2
import numpy as np


def display_images(original_image: np.ndarray, binary_image: np.ndarray) -> None:
    """
    SDisplay images with help of Matplotlib.
    :param original_image: Original image.
    :param binary_image: Binary Image.
    """
    original_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    _, axes = plt.subplots(1, 2, figsize=(12, 6))

    axes[0].imshow(original_rgb)
    axes[0].set_title("Original image")
    axes[0].axis('off')

    axes[1].imshow(binary_image, cmap='gray')
    axes[1].set_title("Binary image")
    axes[1].axis('off')

    plt.show()
