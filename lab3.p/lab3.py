from __future__ import annotations

import argparse
from pathlib import Path
from typing import Tuple

import cv2
import numpy as np
import matplotlib.pyplot as plt


class ImageReadError(Exception):
    """Ошибка чтения изображения."""


def read_image(path: str | Path) -> np.ndarray:
    """Читает изображение (BGR, uint8)."""
    p = Path(path)
    if not p.exists() or not p.is_file():
        raise ImageReadError(f"Файл не найден: {p}")
    img = cv2.imread(str(p), cv2.IMREAD_COLOR)
    if img is None:
        raise ImageReadError(f"Не удалось загрузить: {p}")
    return img


def save_image(path: str | Path, image: np.ndarray) -> None:
    """Сохраняет изображение на диск."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(p), image):
        raise IOError(f"Не удалось сохранить: {p}")


def image_size(image: np.ndarray) -> Tuple[int, int]:
    """Возвращает (width, height)."""
    h, w = image.shape[:2]
    return w, h


def resize_to_match(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    """Делает overlay размера base."""
    H, W = base.shape[:2]
    return cv2.resize(overlay, (W, H), interpolation=cv2.INTER_LINEAR)


def alpha_blend(
    base_bgr: np.ndarray, overlay_bgr: np.ndarray, alpha: float
) -> np.ndarray:
    """Накладывает overlay поверх base с прозрачностью alpha (0..1)."""
    if not (0.0 <= alpha <= 1.0):
        raise ValueError("alpha должен быть в [0, 1].")
    if base_bgr.shape[:2] != overlay_bgr.shape[:2]:
        overlay_bgr = resize_to_match(base_bgr, overlay_bgr)
    return cv2.addWeighted(base_bgr, 1.0 - alpha, overlay_bgr, alpha, 0.0)


def bgr_to_rgb(img_bgr: np.ndarray) -> np.ndarray:
    """BGR → RGB для matplotlib."""
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)


def parse_args() -> argparse.Namespace:
    """Парсит аргументы CLI."""
    parser = argparse.ArgumentParser(
        description="Полупрозрачное наложение одного изображения на другое."
    )
    parser.add_argument("img1", type=str, help="Путь к нижнему изображению")
    parser.add_argument("img2", type=str, help="Путь к накладываемому изображению")
    parser.add_argument("out", type=str, help="Путь для сохранения результата")
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.35,
        help="Прозрачность накладываемого (0..1), по умолчанию 0.35",
    )
    return parser.parse_args()


def print_sizes(img1: np.ndarray, img2: np.ndarray) -> None:
    """Печатает размеры двух изображений."""
    w1, h1 = image_size(img1)
    w2, h2 = image_size(img2)
    print(f"Image1: width={w1}, height={h1}")
    print(f"Image2: width={w2}, height={h2}")


def show_images(
    img1_bgr: np.ndarray, img2_bgr: np.ndarray, result_bgr: np.ndarray
) -> None:
    """Показывает оба исходника и результат в matplotlib."""
    plt.imshow(bgr_to_rgb(img1_bgr))
    plt.title("Image 1 (base)")
    plt.axis("off")
    plt.show()
    plt.imshow(bgr_to_rgb(img2_bgr))
    plt.title("Image 2 (overlay)")
    plt.axis("off")
    plt.show()
    plt.imshow(bgr_to_rgb(result_bgr))
    plt.title("Result (alpha blend)")
    plt.axis("off")
    plt.show()


def main() -> None:
    """Точка входа."""
    args = parse_args()
    try:
        img1 = read_image(args.img1)
        img2 = read_image(args.img2)
        print_sizes(img1, img2)

        result = alpha_blend(img1, img2, alpha=args.alpha)

        show_images(img1, img2, result)
        save_image(args.out, result)
        print(f"Готово. Результат: {args.out}")
    except ImageReadError as e:
        print(f"[Ошибка чтения] {e}")
    except ValueError as e:
        print(f"[Неверные параметры] {e}")
    except Exception as e:
        print(f"[Неожиданная ошибка] {e}")


if __name__ == "__main__":
    main()
