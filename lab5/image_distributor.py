import random
from typing import List, Tuple


class ImageDistributor:
    """Класс для распределения количества изображений по диапазонам дат."""
    
    def __init__(self, min_images: int = 50, max_images: int = 1000) -> None:
        """Инициализирует распределитель изображений"""
        self.min_images = min_images
        self.max_images = max_images
    
    def distribute_images(self, num_ranges: int, target_count: int = None) -> Tuple[int, List[int]]:
        """Распределяет случайное количество изображений по диапазонам
            num_ranges: Количество диапазонов дат
            target_count: Конкретное количество изображений, которые нужно распределить (если None - генерируется случайно)"""
        if target_count is None:
            total_images = random.randint(self.min_images, self.max_images)
        else:
            total_images = target_count
        
        
        images_per_range = [1] * num_ranges
        
        
        remaining_images = total_images - num_ranges
        
        if remaining_images > 0:
            
            weights = [random.random() for _ in range(num_ranges)]
            total_weight = sum(weights)
            
            for i in range(num_ranges):
                share = int(remaining_images * weights[i] / total_weight)
                images_per_range[i] += share
            
            
            distributed_so_far = sum(images_per_range) - num_ranges
            remaining_after_distribution = remaining_images - distributed_so_far
            
            if remaining_after_distribution > 0:
                """Случайно распределяет оставшиеся изображения"""
                indices = random.sample(range(num_ranges), remaining_after_distribution)
                for idx in indices:
                    images_per_range[idx] += 1
        
        return total_images, images_per_range
    
    def distribute_with_user_input(self, num_ranges: int) -> Tuple[int, List[int]]:
        """Распределяет изображения с запросом количества у пользователя
            num_ranges: Количество диапазонов дат"""
        while True:
            try:
                user_input = input(
                    f"Введите количество изображений ({self.min_images}-{self.max_images}): "
                )
                target_count = int(user_input)
                
                if self.min_images <= target_count <= self.max_images:
                    """Прямой вызов без рекурсии, просто возврат результата"""
                    total_images, distribution = self.distribute_images(num_ranges, target_count)
                    return total_images, distribution
                else:
                    print(f"Пожалуйста, введите число от {self.min_images} до {self.max_images}")
            except ValueError:
                print("Пожалуйста, введите корректное число")