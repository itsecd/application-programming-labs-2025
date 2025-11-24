from typing import Tuple
import matplotlib.pyplot as plt
from PIL import Image


def show_image_comparison(
    source_image: Image.Image,
    result_image: Image.Image,
    source_label: str = "Исходное изображение",
    result_label: str = "Обработанное изображение"
) -> None:
    """
    Отображает исходное и обработанное изображения рядом.
    """
    
    figure, axis = plt.subplots(1, 2, figsize=(12, 6))

    source_width, source_height = source_image.size
    axis[0].imshow(source_image)
    axis[0].set_title(f'{source_label}\n{source_width}x{source_height} px', 
                      fontsize=12, fontweight='bold')
    axis[0].axis('off')

    result_width, result_height = result_image.size
    axis[1].imshow(result_image)
    axis[1].set_title(f'{result_label}\n{result_width}x{result_height} px', 
                      fontsize=12, fontweight='bold')
    axis[1].axis('off')

    plt.tight_layout()
    plt.show()


def export_comparison_chart(
    source_image: Image.Image,
    result_image: Image.Image,
    export_path: str,
    source_label: str = "Исходное изображение",
    result_label: str = "Обработанное изображение"
) -> None:
    """
    Сохраняет сравнение изображений в файл.
    """

    figure, axis = plt.subplots(1, 2, figsize=(12, 6))

    source_width, source_height = source_image.size
    axis[0].imshow(source_image)
    axis[0].set_title(f'{source_label}\n{source_width}x{source_height} px', 
                      fontsize=12, fontweight='bold')
    axis[0].axis('off')

    result_width, result_height = result_image.size
    axis[1].imshow(result_image)
    axis[1].set_title(f'{result_label}\n{result_width}x{result_height} px', 
                      fontsize=12, fontweight='bold')
    axis[1].axis('off')

    plt.tight_layout()
    plt.savefig(export_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"График сохранен в: {export_path}")