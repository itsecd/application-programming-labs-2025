from __future__ import annotations
from typing import Any
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

def show_comparison(
    original: NDArray[np.uint8],
    processed: NDArray[np.uint8],
    direction: str,
    intensity: float,
) -> None:
    """Отображает исходное и обработанное изображение рядом.

    Args:
        original (NDArray[np.uint8]): Исходное изображение (RGB).
        processed (NDArray[np.uint8]): Изображение после обработки.
        direction (str): Направление градиента ("horizontal" | "vertical").
        intensity (float): Использованный коэффициент интенсивности.
    """
    plt.figure(figsize=(15, 8))

    plt.subplot(1, 2, 1)
    plt.imshow(original)
    plt.title("Исходное изображение")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(processed)
    plt.title(
        f"С градиентным осветлением\n({direction}, intensity={intensity:.2f})"
    )
    plt.axis("off")

    plt.tight_layout()
    plt.show()