import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def parse_arguments() -> argparse.Namespace:
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description='Наложение изображений с полупрозрачностью')
    parser.add_argument('--background', '-bg', required=True, help='Путь к фоновому изображению')
    parser.add_argument('--foreground', '-fg', required=True, help='Путь к накладываемому изображению')
    parser.add_argument('--output', '-o', required=True, help='Путь для сохранения результата')
    parser.add_argument('--alpha', '-a', type=float, default=0.5, help='Прозрачность накладываемого изображения (0-1)')
    return parser.parse_args()


def load_image(path: str) -> np.ndarray:
    """Загрузка изображения с проверкой"""
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Не удалось загрузить изображение: {path}")
    return img


def resize_foreground(foreground: np.ndarray, background: np.ndarray) -> np.ndarray:
    """Изменение размера накладываемого изображения под размер фонового"""
    bg_height, bg_width = background.shape[:2]
    return cv2.resize(foreground, (bg_width, bg_height))


def blend_images(background: np.ndarray, foreground: np.ndarray, alpha: float) -> np.ndarray:
    
    """Наложение изображений с альфа-смешиванием"""
    
    # Преобразуем в float для точных вычислений
    bg_float = background.astype(float)
    fg_float = foreground.astype(float)
    
    # Альфа-смешивание
    blended = alpha * fg_float + (1 - alpha) * bg_float
    
    return blended.astype(np.uint8)


def create_comparison_plot(background: np.ndarray, foreground: np.ndarray, result: np.ndarray, alpha: float) -> None:
    """Создание сравнительного графика"""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    ax1.imshow(cv2.cvtColor(background, cv2.COLOR_BGR2RGB))
    ax1.set_title(f'Фоновое изображение\n({background.shape[1]}x{background.shape[0]})')
    ax1.axis('off')

    ax2.imshow(cv2.cvtColor(foreground, cv2.COLOR_BGR2RGB))
    ax2.set_title(f'Накладываемое изображение\n({foreground.shape[1]}x{foreground.shape[0]})')
    ax2.axis('off')

    ax3.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    ax3.set_title(f'Результат наложения\n(alpha={alpha})')
    ax3.axis('off')

    plt.tight_layout()
    plt.show()


def save_image(image: np.ndarray, output_path: str) -> None:
    """Сохранение изображения с созданием директорий при необходимости"""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    success = cv2.imwrite(str(path), image)
    if not success:
        raise ValueError(f"Не удалось сохранить изображение: {output_path}")


def main() -> None:
    """Основная функция программы."""
    args = parse_arguments()

    background = load_image(args.background)
    foreground = load_image(args.foreground)

    print(f"Размер фонового изображения: {background.shape[1]}x{background.shape[0]}")
    print(f"Размер накладываемого изображения: {foreground.shape[1]}x{foreground.shape[0]}")
    print(f"Коэффициент прозрачности: {args.alpha}")

    foreground_resized = resize_foreground(foreground, background)
    print(f"Размер накладываемого изображения после изменения: {foreground_resized.shape[1]}x{foreground_resized.shape[0]}")

    result = blend_images(background, foreground_resized, args.alpha)

    create_comparison_plot(background, foreground_resized, result, args.alpha)

    save_image(result, args.output)
    print(f"Результат сохранен в: {args.output}")

if __name__ == "__main__":
    main()