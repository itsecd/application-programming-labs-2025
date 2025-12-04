import cv2
import matplotlib.pyplot as plt
import numpy as np

def resize_image(img: np.ndarray, width, height: int) -> np.ndarray:
    """Изменяет размер изображения на заданный."""
    resized = cv2.resize(img, (width, height))
    return resized

def get_image_size(img: np.ndarray) -> tuple[int, int]:
    """Возвращает размер изображения (высота, ширина)."""
    h, w = img.shape[:2]
    return h, w

def read_image(path: str) -> np.ndarray:
    """Читает изображение из файла."""
    img = cv2.imread(path)
    if img is None:
        print(f"Ошибка: не удалось открыть файл {path}")
    return img

def show_image(first_image, second_image: np.ndarray) -> None:
    """
    Показывает исходное и измененное изображение рядом
    """
    first_rgb = cv2.cvtColor(first_image, cv2.COLOR_BGR2RGB)
    second_rgb = cv2.cvtColor(second_image, cv2.COLOR_BGR2RGB)

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].imshow(first_rgb)
    axs[0].set_title(f"Исходное\n{first_image.shape[1]}x{first_image.shape[0]}")
    axs[0].axis('off')

    axs[1].imshow(second_rgb)
    axs[1].set_title(f"Результат\n{second_image.shape[1]}x{second_image.shape[0]}")
    axs[1].axis('off')

    plt.tight_layout() #Макет интерфейса
    plt.show() # Выводит всё.

def save_image(img: np.ndarray, path: str) -> None:
    """Сохраняет изображение в файл."""
    cv2.imwrite(path, img)
    print(f"Сохранено в: {path}")