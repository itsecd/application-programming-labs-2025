import cv2
import matplotlib.pyplot as plt
import numpy as np


def img_show(img: np.ndarray) -> None:
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()


def img_read(file_path: str) -> np.ndarray:
    img = cv2.imread(file_path)
    shape = img.shape()
    print(
        f"Ширина изображения в пикселях: {shape[1]} \n Высота изображения в пикселях:{shape[0]}"
    )
    return img


def img_rotation(img: np.ndarray, rotation_angle: int) -> np.ndarray:
    shape = img.shape()
    rotation_matrix = cv2.getRotationMatrix2D(
        (shape[1] / 2, shape[0] / 2), rotation_angle, 1.0
    )
    modded_image = cv2.warpAffine(img, rotation_matrix, (shape[1], shape[0]))
    return modded_image


def img_writing(destination_path: str, img: np.ndarray) -> None:
    cv2.imwrite(destination_path, img)
