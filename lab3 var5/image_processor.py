import argparse
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


class ImageProcessor:
    """Класс для обработки изображений."""

    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.image = None

    def load_image(self) -> np.ndarray:
        """
        Загружает изображение из файла.

        :return: массив NumPy с изображением
        :raises: ValueError, Exception
        """
        self.image = cv2.imread(self.input_path)
        if self.image is None:
            raise ValueError(f"Ошибка загрузки изображения из '{self.input_path}'")
        return self.image

    def get_image_info(self) -> str:
        """
        Возвращает информацию о размере изображения.

        :return: строка с информацией о размере
        """
        height, width, _ = self.image.shape
        return f"Размер изображения: {width}x{height}"

    def invert_colors(self) -> np.ndarray:
        """
        Инвертирует цвета изображения.

        :return: массив NumPy с инвертированными цветами
        """
        return 255 - self.image

    def save_image(self, processed_image: np.ndarray) -> None:
        """
        Сохраняет обработанное изображение в файл.

        :param processed_image: массив NumPy с обработанным изображением
        :raises: Exception
        """
        cv2.imwrite(self.output_path, processed_image)

    def display_images(self, original_image: np.ndarray, processed_image: np.ndarray) -> None:
        """
        Демонстрирует исходное и обработанное изображения с помощью Matplotlib.

        :param original_image: исходное изображение
        :param processed_image: обработанное изображение
        """
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.title('Исходное изображение')
        plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.title('Обработанное изображение')
        plt.imshow(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()


def process_image(input_path: str, output_path: str) -> bool:
    """
    Основная функция для обработки изображения.

    :param input_path: путь к исходному изображению
    :param output_path: путь для сохранения обработанного изображения
    :return: True если обработка прошла успешно, False в противном случае
    """
    try:
        processor = ImageProcessor(input_path, output_path)
        loaded_image = processor.load_image()
        image_info = processor.get_image_info()
        inverted_image = processor.invert_colors()
        processor.save_image(inverted_image)
        processor.display_images(loaded_image, inverted_image)
        return True, image_info
    except Exception as e:
        return False, str(e)