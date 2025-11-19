import matplotlib.pyplot as plt
import numpy as np


def reverse_img(img: np.ndarray, vertical: bool = False) -> np.ndarray:
    """Reverse image row by row"""
    return img[:, ::-1] if not vertical else img[::-1, :]


def show(img: np.ndarray, rev_img: np.ndarray) -> None:
    """Show source and reversed image"""

    fig, axes = plt.subplots(1, 2)
    axes[0].imshow(img)
    axes[1].imshow(rev_img)

    axes[0].set_title("Source")
    axes[1].set_title("Result")

    plt.show()
