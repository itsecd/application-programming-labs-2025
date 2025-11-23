import os
from typing import Dict, List, Tuple

import cv2
import numpy as np

class ImageAnalyzer:
    """Класс для анализа изображений."""

    def __init__(self, brightness_ranges: List[Tuple[int, int, str]]):
        self.brightness_ranges = brightness_ranges
        self.range_names = [r[2] for r in brightness_ranges]

    def calculate_brightness_histogram(self, image_path: str) -> Tuple[List[int], List[int], List[int]]:
        """Вычисляет гистограммы яркости по каналам R, G, B."""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return [0] * len(self.brightness_ranges), [0] * len(self.brightness_ranges), [0] * len(self.brightness_ranges)

            # Разделяем на каналы BGR 
            b, g, r = cv2.split(image)

            # Вычисляем среднюю яркость для каждого канала
            r_brightness = self._calculate_channel_brightness(r)
            g_brightness = self._calculate_channel_brightness(g)
            b_brightness = self._calculate_channel_brightness(b)

            return r_brightness, g_brightness, b_brightness

        except Exception:
            return [0] * len(self.brightness_ranges), [0] * len(self.brightness_ranges), [0] * len(self.brightness_ranges)

    def _calculate_channel_brightness(self, channel: np.ndarray) -> List[int]:
        """Вычисляет распределение яркости канала по диапазонам."""
        try:
            # Вычисляем среднюю яркость для канала
            avg_brightness = np.mean(channel)
            
            # Создаем бинарный вектор для всех диапазонов
            result = [0] * len(self.brightness_ranges)
            
            for i, (low, high, _) in enumerate(self.brightness_ranges):
                if low <= avg_brightness <= high:
                    result[i] = 1
                    break
            else:
                # Если не попали ни в один диапазон, выбираем ближайший
                if avg_brightness < self.brightness_ranges[0][0]:
                    result[0] = 1
                else:
                    result[-1] = 1

            return result

        except Exception:
            return [0] * len(self.brightness_ranges)

    def get_brightness_range(self, r_hist: List[int], g_hist: List[int], b_hist: List[int]) -> str:
        """Определяет общий диапазон яркости для изображения."""
        try:
            # Суммируем значения по всем каналам для каждого диапазона
            totals = []
            for i in range(len(self.brightness_ranges)):
                total = r_hist[i] + g_hist[i] + b_hist[i]
                totals.append(total)

            # Находим максимальный диапазон
            max_index = totals.index(max(totals))
            return self.range_names[max_index]

        except Exception:
            return self.range_names[0] if self.range_names else "0-85"

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
        for i, value in enumerate(hist):
            if value == 1:
                return self.range_names[i]
        return self.range_names[0] if self.range_names else "0-85"