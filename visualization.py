import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple


class ImageVisualizer:
    """Класс для визуализации изображений с помощью matplotlib."""

    def show_comparison(
        self, 
        original: np.ndarray, 
        processed: np.ndarray, 
        image_name: str,
        channel_order: Tuple[int, int, int] = (2, 0, 1)
    ) -> None:
        """
        Показывает сравнение оригинального и обработанного изображения.

        Args:
            original: оригинальное изображение
            processed: обработанное изображение
            image_name: имя файла для заголовка
            channel_order: примененный порядок каналов
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        ax1.imshow(original)
        ax1.set_title('Оригинальное изображение')
        ax1.axis('off')

        ax2.imshow(processed)
        
        # Создаем понятное описание порядка каналов
        channel_names = ['R', 'G', 'B']
        mapping = [f"{channel_names[i]}→{channel_names[channel_order[i]]}" 
                  for i in range(3)]
        channel_desc = f"Порядок каналов: {', '.join(mapping)}"
        
        ax2.set_title(f'После смены каналов\n{channel_desc}')
        ax2.axis('off')

        plt.suptitle(f'Обработка изображения: {image_name}', fontsize=14)
        plt.tight_layout()
        plt.show()