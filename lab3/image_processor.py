import os
from typing import Literal, Tuple
import numpy as np
import cv2
import matplotlib.pyplot as plt

BGColor = Literal['black', 'white', 'transparent']


class ImageProcessor:
    """
    Класс ImageProcessor для загрузки, обработки (создание круглого изображения)
    и отображения изображений.

    Attributes:
        filepath (str): Путь к файлу исходного изображения.
        original_image (np.ndarray): Загруженное исходное изображение в формате BGR/BGRA.
        original_shape (Tuple[int, ...]): Форма исходного изображения (высота, ширина, каналы).
        file_size_bytes (int): Размер файла на диске в байтах.
    """

    def __init__(self, filepath: str):
        """
        Инициализирует ImageProcessor, загружая изображение из указанного пути.

        Args:
            filepath (str): Путь к файлу изображения.

        Raises:
            IOError: Если файл изображения не может быть прочитан, не найден
                     или не удается получить его размер.
        """
        self.filepath: str = filepath
        self.original_image: np.ndarray = self._load_image()
        self.original_shape: Tuple[int, ...] = self.original_image.shape

        try:
            self.file_size_bytes: int = os.path.getsize(self.filepath)
        except OSError as e:
            raise IOError(f"Не удалось получить размер файла {self.filepath}: {e}")

    def _load_image(self) -> np.ndarray:
        """
        Приватный метод для загрузки изображения с помощью OpenCV.

        Использует `cv2.imread` с флагом `IMREAD_UNCHANGED` для сохранения
        альфа-канала, если он присутствует.

        Returns:
            np.ndarray: Загруженное изображение в формате BGR/BGRA.

        Raises:
            IOError: Если `cv2.imread` возвращает None (не удалось прочитать файл).
        """
        try:
            image = cv2.imread(self.filepath, cv2.IMREAD_UNCHANGED)
            if image is None:
                raise IOError(f"Не удалось прочитать файл изображения: {self.filepath}. "
                              "Проверьте путь и формат файла.")
            return image
        except cv2.error as e:
            raise IOError(f"Ошибка OpenCV при чтении файла {self.filepath}: {e}")

    def get_image_size_info(self) -> str:
        """
        Возвращает текстовую информацию о размере исходного изображения.
        Включает пиксели и размер файла.

        Returns:
            str: Многострочная строка, содержащая размеры в пикселях и
                 отформатированный размер файла (Б, кБ, МБ).
        """
        height, width = self.original_shape[:2]
        channels = self.original_shape[2] if len(self.original_shape) > 2 else 1

        pixel_info = (f"Размер в пикселях: {width} x {height}, "
                      f"Каналы: {channels}")

        size_info = (f"Размер файла: "
                     f"{self._format_bytes(self.file_size_bytes)}")

        return f"{pixel_info}\n{size_info}"

    def _center_crop_to_square(self, image: np.ndarray) -> np.ndarray:
        """
        Приватный метод для обрезки изображения до квадрата по центру.

        Args:
            image (np.ndarray): Исходное изображение.

        Returns:
            np.ndarray: Обрезанное квадратное изображение.
        """
        h, w = image.shape[:2]
        min_dim = min(h, w)
        start_x = (w - min_dim) // 2
        start_y = (h - min_dim) // 2
        return image[start_y:start_y + min_dim, start_x:start_x + min_dim]

    def make_circular(self, bg_color: BGColor = 'transparent') -> np.ndarray:
        """
        Преобразует изображение в круглое, заполняя область вне круга
        указанным цветом фона (черный, белый или прозрачный).

        Args:
            bg_color (BGColor): Цвет фона для области вне круга.
                                Допустимые значения: 'black', 'white', 'transparent'.
                                По умолчанию 'transparent'.

        Returns:
            np.ndarray: Обработанное изображение в виде круга.
        """
        square_image = self._center_crop_to_square(self.original_image)
        height, width = square_image.shape[:2]
        center = (width // 2, height // 2)
        radius = width // 2

        mask = np.zeros((height, width), dtype=np.uint8)
        cv2.circle(mask, center, radius, 255, -1)

        if bg_color == 'transparent':
            if square_image.shape[2] == 3:
                image_bgra = cv2.cvtColor(square_image, cv2.COLOR_BGR2BGRA)
            else:
                image_bgra = square_image

            b, g, r, a = cv2.split(image_bgra)
            new_alpha = cv2.bitwise_and(a, mask)
            result_image = cv2.merge((b, g, r, new_alpha))

        else:
            if square_image.shape[2] == 4:
                image_bgr = cv2.cvtColor(square_image, cv2.COLOR_BGRA2BGR)
            else:
                image_bgr = square_image

            background_color = (255, 255, 255) if bg_color == 'white' else (0, 0, 0)
            background = np.full_like(image_bgr, background_color)

            inverse_mask = cv2.bitwise_not(mask)
            background_ring = cv2.bitwise_and(background, background, mask=inverse_mask)

            foreground_circle = cv2.bitwise_and(image_bgr, image_bgr, mask=mask)

            result_image = cv2.add(background_ring, foreground_circle)

        return result_image

    def _convert_for_matplotlib(self, image_data: np.ndarray) -> np.ndarray:
        """
        Приватный метод для конвертации изображения из формата OpenCV (BGR/BGRA)
        в формат Matplotlib (RGB/RGBA).

        Matplotlib по умолчанию ожидает RGB/RGBA, тогда как OpenCV использует BGR/BGRA.

        Args:
            image_data (np.ndarray): Изображение в формате BGR или BGRA.

        Returns:
            np.ndarray: Изображение в формате RGB или RGBA, готовое для Matplotlib.
        """
        if len(image_data.shape) == 2:
            return image_data

        channels = image_data.shape[2]
        if channels == 3:
            return cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)
        if channels == 4:
            return cv2.cvtColor(image_data, cv2.COLOR_BGRA2RGBA)
        return image_data

    def display_comparison(self, processed_image: np.ndarray) -> None:
        """
        Отображает исходное изображение и обработанное (круглое) изображение
        рядом с помощью Matplotlib для визуального сравнения.

        Args:
            processed_image (np.ndarray): Обработанное круглое изображение.
        """
        original_display = self._convert_for_matplotlib(self.original_image)
        processed_display = self._convert_for_matplotlib(processed_image)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        ax1.imshow(original_display)
        ax1.set_title(f"Оригинал ({self.original_shape[1]}x{self.original_shape[0]} px)")
        ax1.axis("off")

        ax2.imshow(processed_display)
        ax2.set_title("Результат (Круглое)")
        ax2.axis("off")

        plt.suptitle(f"Сравнение изображений: {self.filepath}")
        plt.tight_layout()
        plt.show()

    def save_result_image(self, output_path: str, image_to_save: np.ndarray) -> None:
        """
        Сохраняет указанное изображение в файл по заданному пути.

        Args:
            output_path (str): Путь, по которому будет сохранен файл.
            image_to_save (np.ndarray): Изображение (NumPy массив), которое нужно сохранить.

        Raises:
            IOError: Если не удается сохранить файл (например, из-за неверного пути
                     или проблем с разрешениями).
        """
        try:
            success = cv2.imwrite(output_path, image_to_save)
            if not success:
                raise IOError(f"Не удалось сохранить файл изображения: {output_path}. "
                              "Проверьте путь и права на запись.")
        except cv2.error as e:
            raise IOError(f"Ошибка OpenCV при сохранении файла {output_path}: {e}")

    @staticmethod
    def _format_bytes(size_bytes: int) -> str:
        """
        Форматирует байты в читаемую строку (Б, кБ, МБ...).

        Args:
            size_bytes (int): Размер в байтах.

        Returns:
            str: Отформатированная строка.
        """
        if size_bytes == 0:
            return "0 Б"
        suffixes = ['Б', 'кБ', 'МБ', 'ГБ', 'ТБ']
        i = 0
        size_float = float(size_bytes)
        while size_float >= 1024 and i < len(suffixes) - 1:
            size_float /= 1024
            i += 1

        if i == 0:
            return f"{size_float:.0f} {suffixes[i]}"
        else:
            return f"{size_float:.2f} {suffixes[i]}"