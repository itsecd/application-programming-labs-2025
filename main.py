import argparse
import cv2
import numpy as np
import os
import sys



def parse_args() -> argparse.Namespace:

    p = argparse.ArgumentParser(description="Сделать изображение полутоновым")

    p.add_argument("-i",
                   "--input",
                   required=True,
                   help="Путь к исходному изображению")

    p.add_argument("-o",
                   "--output",
                   default="Save_Result",
                   help="Путь для сохранения результата")

    return p.parse_args()

def read_image(path: str) -> np.ndarray:

    if not os.path.exists(path):
        print(f"Файл {path} не найден")
        sys.exit(1)

    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)  # возможно 1,3 или 4 канала

    if img is None:
        print(f"Не удалось прочитать изображение с помощью OpenCV: {path}")
        sys.exit(1)

    return img

def print_image_info(img: np.ndarray) -> None:
    shape = img.shape
    print(f"Размер исходного файла: {shape[1]}×{shape[0]}")

def to_grayscale(img: np.ndarray) -> np.ndarray:

    if img.ndim == 2:
        if img.dtype != np.uint8:
            if np.issubdtype(img.dtype, np.floating):
                gray = np.clip(img * 255, 0, 255).astype(np.uint8)
                return gray
            else:
                gray = img.astype(np.uint8)
                return gray
        return img.copy()


    shape = img.shape

    if shape[2] == 4:
        bgr = img[:, :, :3]
    else:
        bgr = img
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    return gray

def show_pair(original: np.ndarray, gray: np.ndarray) -> None:
    plt.figure()

    plt.subplot(1, 2, 1)
    if original.ndim == 2:
        plt.imshow(original, cmap="gray")
    else:
        if original.shape[2] == 4:
            bgr = original[:, :, :3]
        else:
            bgr = original
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        plt.imshow(rgb)

    plt.title("Исходное")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(gray, cmap="gray")
    plt.title("Полутоновое")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

def save_image(path: str, img: np.ndarray) -> None:

    if img.dtype != np.uint8:
        if np.issubdtype(img.dtype, np.floating):
            img_to_save = np.clip(img * 255.0, 0, 255).astype(np.uint8)
        else:
            img_to_save = img.astype(np.uint8)
    else:
        img_to_save = img

    cv2.imwrite(path, img_to_save)

def main():
    args = parse_args()

    img = read_image(args.input)

    print_image_info(img)

    gray = to_grayscale(img)

    show_pair(img, gray)

    save_image(args.output, gray)

if __name__ == "__main__":
    main()