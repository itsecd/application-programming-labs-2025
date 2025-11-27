import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys
import os

def resize_by_height(img, height):
    return cv2.resize(img, (int(img.shape[1] * height / img.shape[0]), height))

def resize_by_width(img, width):
    return cv2.resize(img, (width, int(img.shape[0] * width / img.shape[1])))

def ensure_3_channels(img):
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if img.shape[2] == 4:
        img = img[:, :, :3]
    return img

def main():
    parser = argparse.ArgumentParser(description="Соединение двух изображений с демонстрацией")
    parser.add_argument("image1", type=str, help="Путь к первому изображению")
    parser.add_argument("image2", type=str, help="Путь ко второму изображению")
    parser.add_argument("output", type=str, help="Путь для сохранения результата")
    parser.add_argument("--axis", type=str, default="horizontal", choices=["horizontal", "vertical"],
                        help="Направление соединения: horizontal или vertical")
    args = parser.parse_args()

    if not os.path.exists(args.image1) or not os.path.exists(args.image2):
        print("Ошибка: один из входных файлов не найден!")
        sys.exit(1)

    img1 = cv2.imread(args.image1)
    img2 = cv2.imread(args.image2)

    if img1 is None or img2 is None:
        print("Ошибка: не удалось загрузить изображения")
        sys.exit(1)

    img1 = ensure_3_channels(img1)
    img2 = ensure_3_channels(img2)

    print(f"Размер первого изображения (H×W×C): {img1.shape}")
    print(f"Размер второго изображения (H×W×C): {img2.shape}")

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    plt.title("Исходное изображение 1")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    plt.title("Исходное изображение 2")
    plt.axis('off')
    plt.show()

    if args.axis == "horizontal":
        height = min(img1.shape[0], img2.shape[0])
        img1_resized = resize_by_height(img1, height)
        img2_resized = resize_by_height(img2, height)
        result = np.hstack((img1_resized, img2_resized))
    else:
        width = min(img1.shape[1], img2.shape[1])
        img1_resized = resize_by_width(img1, width)
        img2_resized = resize_by_width(img2, width)
        result = np.vstack((img1_resized, img2_resized))

    print(f"Размер итогового изображения (H×W×C): {result.shape}")

    plt.figure(figsize=(12, 6))
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title("Соединённое изображение")
    plt.axis('off')
    plt.show()

    if cv2.imwrite(args.output, result):
        print(f"Результат сохранён в: {args.output}")
    else:
        print("Ошибка: не удалось сохранить результат!")

if __name__ == "__main__":
    main()