from typing import Tuple
import matplotlib.pyplot as plt
from PIL import Image


def display_images_comparison(
    original_img: Image.Image,
    processed_img: Image.Image,
    original_title: str = "Исходное изображение",
    processed_title: str = "Обработанное изображение"
) -> None:
    """
    Отображает исходное и обработанное изображения рядом.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    original_width, original_height = original_img.size
    axes[0].imshow(original_img)
    axes[0].set_title(f'{original_title}\n{original_width}x{original_height} px', 
                      fontsize=12, fontweight='bold')
    axes[0].axis('off')
    
    processed_width, processed_height = processed_img.size
    axes[1].imshow(processed_img)
    axes[1].set_title(f'{processed_title}\n{processed_width}x{processed_height} px', 
                      fontsize=12, fontweight='bold')
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.show()


def save_comparison_plot(
    original_img: Image.Image,
    processed_img: Image.Image,
    output_path: str,
    original_title: str = "Исходное изображение",
    processed_title: str = "Обработанное изображение"
) -> None:
    """
    Сохраняет сравнение изображений в файл.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    original_width, original_height = original_img.size
    axes[0].imshow(original_img)
    axes[0].set_title(f'{original_title}\n{original_width}x{original_height} px', 
                      fontsize=12, fontweight='bold')
    axes[0].axis('off')
    
    processed_width, processed_height = processed_img.size
    axes[1].imshow(processed_img)
    axes[1].set_title(f'{processed_title}\n{processed_width}x{processed_height} px', 
                      fontsize=12, fontweight='bold')
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"График сохранен в: {output_path}")
    
    