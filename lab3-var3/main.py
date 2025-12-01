import argparse
import os
import sys
import matplotlib.pyplot as plt
import cv2
from utils import ensure_3_channels, concatenate_images
from typing import Tuple

def load_image(path: str) -> cv2.Mat:
    """Загружает изображение и приводит к 3-канальному формату."""
    if not os.path.exists(path):
        print(f"Ошибка: файл {path} не найден!")
        sys.exit(1)
    img = cv2.imread(path)
    if img is None:
        print(f"Ошибка: не удалось загрузить {path}")
        sys.exit(1)
    return ensure_3_channels(img)

def show_images_side_by_side(images: Tuple[cv2.Mat, ...], titles: Tuple[str, ...]) -> None:
    """Отображает несколько изображений в одном окне."""
    n = len(images)
    plt.figure(figsize=(6 * n, 6))
    for i, (img, title) in enumerate(zip(images, titles), 1):
        plt.subplot(1, n, i)
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.title(title)
        plt.axis('off')
    plt.show()

def main() -> None:
    parser = argparse.ArgumentParser(description="Соединение двух изображений")
    parser.add_argument("image1", type=str, help="Путь к первому изображению")
    parser.add_argument("image2", type=str, help="Путь ко второму изображению")
    parser.add_argument("output", type=str, help="Путь для сохранения результата")
    parser.add_argument("--axis", type=str, default="horizontal", choices=["horizontal", "vertical"],
                        help="Направление соединения: horizontal или vertical")
    args = parser.parse_args()

    img1 = load_image(args.image1)
    img2 = load_image(args.image2)

    result = concatenate_images(img1, img2, axis=args.axis)

    print(f"Размер итогового изображения (H×W×C): {result.shape}")

    show_images_side_by_side((img1, img2, result),
                             ("Исходное 1", "Исходное 2", "Результат"))

    if cv2.imwrite(args.output, result):
        print(f"Результат сохранён в: {args.output}")
    else:
        print("Ошибка: не удалось сохранить результат!")

if __name__ == "__main__":
    main()