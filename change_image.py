import cv2
import numpy as np

def change_image(img: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Изменение изображения
    """
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_changed = img_rgb[:, :, [2, 1, 0]]
    return img_rgb, img_changed
