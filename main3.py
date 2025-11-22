import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from typing import NoReturn, Any


def apply_pixel_art(img: np.ndarray, scale_factor: float = 0.1) -> np.ndarray:
    """
    Применяет эффект пиксел-арта к изображению.
    """
    if scale_factor <= 0 or scale_factor >= 1:
        raise ValueError("Коэффициент масштабирования должен быть в диапазоне (0, 1).")

    h, w = img.shape[:2]
    small_h = int(h * scale_factor)
    small_w = int(w * scale_factor)

    if small_h < 1 or small_w < 1:
        raise ValueError("Коэффициент масштабирования слишком мал для заданного изображения.")

    small_img = cv2.resize(img, (small_w, small_h), interpolation=cv2.INTER_AREA)
    pixel_art_img = cv2.resize(small_img, (w, h), interpolation=cv2.INTER_NEAREST)

    return pixel_art_img


def _display_images(original: np.ndarray, result: np.ndarray, scale: float) -> None:
    """
    Отображает два изображения рядом: исходное и результат.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    axes[0].imshow(original)
    axes[0].set_title("Исходное изображение")
    axes[0].axis("off")

    axes[1].imshow(result)
    axes[1].set_title(f"Пиксел-арт (scale={scale})")
    axes[1].axis("off")

    plt.tight_layout()
    plt.show()


def main() -> None:
    """
    Основная функция программы.
    Обрабатывает аргументы командной строки, загружает изображение,
    применяет эффект пиксел-арта, отображает результат и сохраняет его в файл.
    """
    
    input_path: str = sys.argv[1]
    output_path: str = sys.argv[2]
    scale_factor: float = float(sys.argv[3]) if len(sys.argv) > 3 else 0.1

    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Файл не найден: {input_path}")

        img = cv2.imread(input_path)
        if img is None:
            raise ValueError(f"Не удалось загрузить изображение: {input_path}. Проверьте формат файла.")

        print(f"Размер исходного изображения: {img.shape[1]}x{img.shape[0]} пикселей")

        pixel_art_img = apply_pixel_art(img, scale_factor)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pixel_art_rgb = cv2.cvtColor(pixel_art_img, cv2.COLOR_BGR2RGB)

        _display_images(img_rgb, pixel_art_rgb, scale_factor)

        if not cv2.imwrite(output_path, pixel_art_img):
            raise IOError(f"Не удалось сохранить результат в: {output_path}")

        print(f"Результат успешно сохранён в: {output_path}")

    except (FileNotFoundError, ValueError, IOError) as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()