import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from typing import Optional


def visualize_comparison(original_image: npt.NDArray[np.uint8], 
                        processed_image: npt.NDArray[np.uint8], 
                        noise_intensity: float,
                        figsize: Tuple[int, int] = (12, 6)) -> None:
    """
    Визуализирует сравнение исходного и обработанного изображения
    
    Args:
        original_image: Исходное изображение
        processed_image: Обработанное изображение
        noise_intensity: Интенсивность шума для заголовка
        figsize: Размер фигуры
    """
    plt.figure(figsize=figsize)
    
    plt.subplot(1, 2, 1)
    plt.imshow(original_image)
    plt.title('Исходное изображение')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(processed_image)
    plt.title(f'Изображение с белым шумом\n(интенсивность: {noise_intensity})')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()


def visualize_single_image(image: npt.NDArray[np.uint8], 
                          title: str = "Изображение",
                          figsize: Tuple[int, int] = (8, 6)) -> None:
    """
    Визуализирует одно изображение
    
    Args:
        image: Изображение для отображения
        title: Заголовок изображения
        figsize: Размер фигуры
    """
    plt.figure(figsize=figsize)
    plt.imshow(image)
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()