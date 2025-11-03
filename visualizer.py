import matplotlib.pyplot as plt
import cv2

def show_comparison(original_img, puzzle_img, n):
    """Показывает сравнение исходного изображения и паззла"""
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB))
    plt.title('Исходное изображение')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(puzzle_img, cv2.COLOR_BGR2RGB))
    plt.title(f'Паззл ({n}×{n} частей)')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()