from pathlib import Path
from typing import Tuple

import cv2
import matplotlib.pyplot as plt

class ImageProcessor:
    """
    Класс для обработки изображений: чтение, преобразование, сохранение.
    """

    def __init__(self, input_path: Path, output_path: Path):
        """
        Инициализация класса с путями к файлам.
        """
        self.input_path = input_path
        self.output_path = output_path
        self.image = None
        self.binary_image = None

    def load_image(self) -> None:
        """
        Загрузка изображения.
        """
        self.image = cv2.imread(str(self.input_path))
        if self.image is None:
            raise FileNotFoundError(
                f"Не удалось загрузить изображение по пути: {self.input_path}"
            )

    def get_image_size(self) -> Tuple[int, int]:
        """
        Возвращает размер изображения (ширина, высота).
        """
        if self.image is None:
            raise ValueError("Изображение не загружено.")
        height, width = self.image.shape[:2]
        return width, height

    def convert_to_binary(self) -> None:
        """
        Преобразует изображение в бинарное.
        """
        if self.image is None:
            raise ValueError("Изображение не загружено.")
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, self.binary_image = cv2.threshold(gray_image, 70, 255, cv2.THRESH_BINARY)

    def save_image(self) -> None:
        """
        Сохранение бинарного изображения в файл.
        """
        if self.binary_image is None:
            raise ValueError("Бинарное изображение не создано.")
        success = cv2.imwrite(str(self.output_path), self.binary_image)
        if not success:
            raise IOError(
                f"Не удалось сохранить изображение по пути: {self.output_path}"
            )

    def display_images(self) -> None:
        """
        Отображает исходное и бинарное изображение с помощью matplotlib.
        """
        if self.image is None or self.binary_image is None:
            raise ValueError("Изображения для отображения отсутствуют.")
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        plt.title("Исходное изображение")
        plt.axis("off")

        plt.subplot(1, 2, 2)
        plt.imshow(self.binary_image, cmap="gray")
        plt.title("Бинарное изображение")
        plt.axis("off")

        plt.show()
