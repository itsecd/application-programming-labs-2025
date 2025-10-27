import random
from typing import List, Tuple


class ImageDistributor:
    """Класс для распределения количества изображений по диапазонам дат."""

    def __init__(self, min_images: int = 50, max_images: int = 1000) -> None:
        self.min_images = min_images
        self.max_images = max_images

    def distribute_images(self, num_ranges: int, target_count: int = None) -> Tuple[int, List[int]]:
        """Распределяет изображения по диапазонам"""
        if target_count is None:
            total_images = random.randint(self.min_images, self.max_images)
        else:
            total_images = target_count

        # Простое распределение: каждому диапазону минимум 1
        distribution = [1] * num_ranges
        remaining = total_images - num_ranges

        # Случайно распределяем оставшиеся
        for i in range(remaining):
            idx = random.randint(0, num_ranges - 1)
            distribution[idx] += 1

        return total_images, distribution

    def distribute_with_user_input(self, num_ranges: int) -> Tuple[int, List[int]]:
        """Распределяет с запросом у пользователя"""
        while True:
            try:
                user_input = input(f"Введите количество изображений ({self.min_images}-{self.max_images}): ")
                target_count = int(user_input)

                if self.min_images <= target_count <= self.max_images:
                    return self.distribute_images(num_ranges, target_count)
                else:
                    print(f"Введите число от {self.min_images} до {self.max_images}")
            except ValueError:
                print("Введите корректное число")