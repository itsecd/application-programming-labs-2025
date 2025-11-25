import argparse
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def check_args(input_path: str, threshold: int) -> None:
    """
    проверка аргументов
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"файл не найден: {input_path}")

    if not 0 <= threshold <= 255:
        raise ValueError("порог должен быть в диапазоне от 0 до 255")


def read_image(image_path: str) -> np.ndarray:
    """
    загрузка изображения
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"не удалось загрузить изображение: {image_path}")
    return img


def binarize_image(img: np.ndarray, threshold: int) -> np.ndarray:
    """
    бинаризация
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return binary


def save_image(image: np.ndarray, output_path: str) -> None:
    """
    сохранение нового изображения
    """
    if os.path.exists(output_path):
        raise FileExistsError(f"файл уже существует: {output_path}")

    if not cv2.imwrite(output_path, image):
        raise ValueError(f"ошибка при сохранении изображения: {output_path}")


def display_images(original_img: np.ndarray, binary_img: np.ndarray, original_path: str, threshold: int) -> None:
    """
    отображение исходного и бинарного изображений
    """
    original_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    axes[0].imshow(original_rgb)
    axes[0].set_title(f'исходное изображение\n{os.path.basename(original_path)}')
    axes[0].axis('off')

    axes[1].imshow(binary_img, cmap='gray')
    axes[1].set_title(f'бинарное изображение\nпорог: {threshold}')
    axes[1].axis('off')

    plt.tight_layout()
    plt.show()


def main():

    parser = argparse.ArgumentParser(description='преобразование изображения в бинарное')
    parser.add_argument('-i', '--input', type=str, required=True, help='путь к исходному изображению')
    parser.add_argument('-o', '--output', type=str, help='путь для сохранения изображения (опционально)')
    parser.add_argument('-th', '--threshold', type=int, default=127, help='порог для бинаризации')
    args = parser.parse_args()

    try:
        check_args(args.input, args.threshold)

        original_img = read_image(args.input)

        h, w, c = original_img.shape
        print(f"размер: {w}x{h}, каналы: {c}")

        binary_img = binarize_image(original_img, args.threshold)

        if args.output:
            save_image(binary_img, args.output)
            print(f"изображение сохранено: {args.output}")
        else:
            print("без сохранения")


        print(f"обработано изображение {os.path.basename(args.input)}")
        print(f"порог:      {args.threshold}")

        display_images(original_img, binary_img, args.input, args.threshold)


    except Exception as e:
        print(f"ошибочка: {e}")

if __name__ == "__main__":
    main()
