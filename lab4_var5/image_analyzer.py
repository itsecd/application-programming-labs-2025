"""Модуль для анализа изображений и вычисления характеристик."""
import cv2
import os


class ImageAnalyzer:
    """Класс для анализа изображений."""

    def __init__(self):
        """Инициализация анализатора изображений."""
        pass

    def calculate_brightness(self, image_path):
        """
        Вычисляет среднюю яркость изображения по всем каналам.

        Args:
            image_path: Путь к изображению

        Returns:
            float: Средняя яркость изображения
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Не удалось загрузить изображение: {image_path}")

            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            brightness = image_rgb.mean()

            return round(brightness, 2)

        except Exception as e:
            raise RuntimeError(
                f"Ошибка при вычислении яркости для {image_path}: {e}"
            )

    def process_images_brightness(self, image_paths):
        """
        Вычисляет яркость для списка изображений.

        Args:
            image_paths: Список путей к изображениям

        Returns:
            list: Список значений яркости
        """
        brightness_values = []

        for image_path in image_paths:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Файл не найден: {image_path}")

            brightness = self.calculate_brightness(image_path)
            brightness_values.append(brightness)

        return brightness_values