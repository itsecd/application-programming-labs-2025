import os
from typing import Dict, List, Tuple

import cv2
import numpy as np

class ImageAnalyzer:
    """Класс для анализа изображений."""

    def __init__(self):
        self.brightness_ranges = ["0-85", "86-170", "171-255"]

    def calculate_brightness_histogram(self, image_path: str) -> Tuple[List[int], List[int], List[int]]:
        """Вычисляет гистограммы яркости по каналам R, G, B."""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return [0, 0, 0], [0, 0, 0], [0, 0, 0]

            # Разделяем на каналы BGR (OpenCV использует BGR по умолчанию)
            b, g, r = cv2.split(image)

            # Вычисляем среднюю яркость для каждого канала
            r_brightness = self._calculate_channel_brightness(r)
            g_brightness = self._calculate_channel_brightness(g)
            b_brightness = self._calculate_channel_brightness(b)

            return r_brightness, g_brightness, b_brightness

        except Exception as e:
            print(f"  Предупреждение: ошибка анализа {os.path.basename(image_path)}")
            return [0, 0, 0], [0, 0, 0], [0, 0, 0]

    def _calculate_channel_brightness(self, channel: np.ndarray) -> List[int]:
        """Вычисляет распределение яркости канала по диапазонам."""
        try:
            # Вычисляем среднюю яркость для канала
            avg_brightness = np.mean(channel)

            # Определяем диапазон и возвращаем бинарный вектор
            if avg_brightness <= 85:
                return [1, 0, 0]  
            elif avg_brightness <= 170:
                return [0, 1, 0]  
            else:
                return [0, 0, 1]  

        except Exception as e:
            return [0, 0, 0]

    def get_brightness_range(self, r_hist: List[int], g_hist: List[int], b_hist: List[int]) -> str:
        """Определяет общий диапазон яркости для изображения."""
        try:
            # Суммируем значения по всем каналам для каждого диапазона
            total_low = r_hist[0] + g_hist[0] + b_hist[0]  
            total_medium = r_hist[1] + g_hist[1] + b_hist[1] 
            total_high = r_hist[2] + g_hist[2] + b_hist[2]  

            # Находим максимальный диапазон
            totals = [total_low, total_medium, total_high]
            max_index = totals.index(max(totals))

            return self.brightness_ranges[max_index]

        except Exception as e:
            return "0-85"  

    def get_brightness_stats(self, image_path: str) -> Dict:
        """Возвращает статистику яркости для одного изображения."""
        r_hist, g_hist, b_hist = self.calculate_brightness_histogram(image_path)
        brightness_range = self.get_brightness_range(r_hist, g_hist, b_hist)

        return {
            'image_path': image_path,
            'r_histogram': r_hist,
            'g_histogram': g_hist,
            'b_histogram': b_hist,
            'brightness_range': brightness_range,
            'r_channel': self._hist_to_range(r_hist),
            'g_channel': self._hist_to_range(g_hist),
            'b_channel': self._hist_to_range(b_hist)
        }

    def _hist_to_range(self, hist: List[int]) -> str:
        """Конвертирует гистограмму в текстовый диапазон."""
        if hist[0] == 1:
            return "0-85"
        elif hist[1] == 1:
            return "86-170"
        else:
            return "171-255"