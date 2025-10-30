import cv2
import os


def save_noisy_images(noisy_images, output_dir) -> None:
    """
    функция для сохранения в файл картинок с белым шумом
    """
    for i, img in enumerate(noisy_images):
        filename = os.path.join(output_dir, f"white_noise_{i}.jpg")
        cv2.imwrite(filename, img)
