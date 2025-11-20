import matplotlib.pyplot as plt


class ImageVisualizer:
    """Класс для визуализации изображений с помощью matplotlib."""

    def show_comparison(self, original, processed, image_name):
        """
        Показывает сравнение оригинального и обработанного изображения.

        Args:
            original: оригинальное изображение
            processed: обработанное изображение
            image_name: имя файла для заголовка
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        ax1.imshow(original)
        ax1.set_title('Оригинальное изображение')
        ax1.axis('off')

        ax2.imshow(processed)
        ax2.set_title('После смены каналов (R->G, G->B, B->R)')
        ax2.axis('off')

        plt.suptitle(f'Обработка изображения: {image_name}', fontsize=14)
        plt.tight_layout()
        plt.show()
