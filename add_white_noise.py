import numpy as np


def add_white_noise(images: list[np.ndarray]) -> list[np.ndarray]:
    """
    функция для добавления белого шума на картинки
    """
    noisy_images = []
    for img in images:
        new_img = img + 3 * img.std() * np.random.random(img.shape)
        new_img = np.clip(new_img, 0, 255).astype(np.uint8)
        noisy_images.append(new_img)
    return noisy_images
