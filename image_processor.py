import os

import cv2


class ImageProcessor:
    """Класс для обработки изображений."""

    def load_image(self, image_path):
        """
        Загружает изображение из файла.

        Args:
            image_path: путь к изображению

        Returns:
            изображение в формате numpy array или None при ошибке
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Файл {image_path} не существует")

        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Не удалось загрузить изображение {image_path}")
            
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image_rgb

    def swap_channels(self, image_path):
        """
        Меняет местами каналы изображения (R, G, B).

        Args:
            image_path: путь к исходному изображению

        Returns:
            кортеж (оригинальное изображение, обработанное изображение)
        """
        original_image = self.load_image(image_path)
        processed_image = original_image.copy()

        processed_image[:, :, 0], processed_image[:, :, 1], processed_image[:, :, 2] = \
            original_image[:, :, 2], original_image[:, :, 0], original_image[:, :, 1]

        return original_image, processed_image

    def save_image(self, image, output_path):
        """
        Сохраняет изображение в файл.

        Args:
            image: изображение для сохранения
            output_path: путь для сохранения
        """
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, image_bgr)