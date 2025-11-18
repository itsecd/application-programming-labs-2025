import cv2
import numpy
import matplotlib.pyplot as plt


def show_image(first_image: numpy.ndarray, second_image: numpy.ndarray) -> None:
    """
    ввыводим изображение при помощи matplotlib
    """
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].imshow(first_image)
    axs[0].axis('off')

    axs[1].imshow(second_image)
    axs[1].axis('off')

    plt.tight_layout()
    plt.show()


def change_size(image: numpy.ndarray, new_size: tuple[int, int]) -> numpy.ndarray:
    """
    изменяем ширину и высоту изображения
    """
    return cv2.resize(
        image,
        new_size,
        interpolation=cv2.INTER_LINEAR
    )


def size_format(size: str) -> tuple[int, int]:
    """
    приводим строчное обозначение размера в формат кортежа
    """
    size = size.split('X')
    if len(size) != 2:
        raise ValueError('размер изображения должен быть в формате widthXheight')
    width = int(size[0])
    height = int(size[1])
    return width, height