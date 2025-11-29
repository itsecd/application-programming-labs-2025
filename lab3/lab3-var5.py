import argparse
from pathlib import Path
import cv2
import matplotlib.pyplot as plt
import numpy as np

def parse_args() -> argparse.Namespace:
    """
    Разбор аргументы командной строки
    """
    parser = argparse.ArgumentParser(description="ЛР 3: инверсия цветов изображения")
    parser.add_argument("--input", required=True, help="Путь к исходному изображению")
    parser.add_argument("--output", required=True, help="Путь к сохранённому изображению")
    return parser.parse_args()


def load_image(path: Path) -> np.ndarray:
    """
    Загрузка изображение через OpenCV и возвращение numpy-массив
    """
    img = cv2.imread(str(path))

    if img is None:
        raise ValueError("Ошибка: изображение не найдено. Проверьте путь!")

    return img


def invert_colors(img: np.ndarray) -> np.ndarray:
    """
    Инвертирование цвета: новый = 255 - старый.
    """
    return 255 - img


def show_images(original: np.ndarray, inverted: np.ndarray) -> None:
    """
    Показ двух изображений рядом через matplotlib.
    """
    # Перевод изображений из BGR (OpenCV) в RGB (matplotlib)
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    inverted_rgb = cv2.cvtColor(inverted, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.title("Исходное изображение")
    plt.imshow(original_rgb)
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Инвертированное изображение")
    plt.imshow(inverted_rgb)
    plt.axis("off")

    plt.show()


def save_image(path: Path, img: np.ndarray) -> None:
    """
    Сохранение изображения через OpenCV.
    """
    cv2.imwrite(str(path), img)


def main() -> None:
    """
    Главная функция
    """
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    # 1. Загрузка изображения
    img = load_image(input_path)

    # 2. Вывод размера
    print(f"Размер изображения (height, width, channels): {img.shape}")

    # 3. Инверсия цветов
    inverted_img = invert_colors(img)

    # 4. Показ
    show_images(img, inverted_img)

    # 5. Сохранение
    save_image(output_path, inverted_img)

    print(f"Результат сохранён в: {output_path}")


if __name__ == "__main__":
    main()