import random
from typing import List, Tuple


class ImageDistributor:
    """Класс для распределения количества изображений по диапазонам дат."""
    
    def __init__(self, min_images: int = 50, max_images: int = 1000) -> None:
        """Инициализирую распределитель изображений"""
        self.min_images = min_images
        self.max_images = max_images
    
    def distribute_images(self, num_ranges: int, target_count: int = None) -> Tuple[int, List[int]]:
        """Распределяет случайное количество изображений по диапазонам
            num_ranges: Количество диапазонов дат
            target_count: Конкретное количество изображений (если None - генерируется случайно)"""
        if target_count is None:
            total_images = random.randint(self.min_images, self.max_images)
        else:
            total_images = target_count
        
        
        images_per_range = [1] * num_ranges
        
        """Распределение оставшиеся изображения случайным образом"""
        remaining_images = total_images - num_ranges
        
        for _ in range(remaining_images):
            range_index = random.randint(0, num_ranges - 1)
            images_per_range[range_index] += 1
        
        return total_images, images_per_range
    
    def distribute_with_user_input(self, num_ranges: int) -> Tuple[int, List[int]]:
        """Распределяю изображения с запросом количества у пользователя
            num_ranges: Количество диапазонов дат"""
        while True:
            try:
                user_input = input(
                    f"Введите количество изображений ({self.min_images}-{self.max_images}): "
                )
                target_count = int(user_input)
                
                if self.min_images <= target_count <= self.max_images:
                    return self.distribute_images(num_ranges, target_count)
                else:
                    print(f"Пожалуйста, введите число от {self.min_images} до {self.max_images}")
            except ValueError:
                print("Пожалуйста, введите корректное число")