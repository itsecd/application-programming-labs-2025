import argparse
import os
from typing import Tuple, Optional

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image




def parse_arguments() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки

    Returns:
        argparse.Namespace: Объект с распарсенными аргументами
    """
    parser = argparse.ArgumentParser(description="Наложение белого шума на изображение")
    parser.add_argument(
        "--input", "-i", type=str, required=True, help="Путь к исходному изображению"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="output_image.jpg",
        help="Путь для сохранения результата (по умолчанию: output_image.jpg)",
    )
    parser.add_argument(
        "--noise-intensity",
        "-n",
        type=float,
        default=0.1,
        help="Интенсивность шума от 0.0 до 1.0 (по умолчанию: 0.1)",
    )
    parser.add_argument(
        "--seed",
        "-s",
        type=int,
        default=None,
        help="Seed для генератора случайных чисел (по умолчанию: None)",
    )
    parser.add_argument(
        "--show-plots", action="store_true", help="Показать графики с результатами"
    )

    return parser.parse_args()


def load_image(image_path: str) -> Tuple[np.ndarray, str]:
    """
    Загрузка изображения из файла

    Args:
        image_path: путь к файлу изображения

    Returns:
        Tuple[np.ndarray, str]: массив изображения и режим цветового пространства

    Raises:
        FileNotFoundError: если файл не существует
        ValueError: если файл не является изображением
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Файл {image_path} не найден")

    try:
        img = Image.open(image_path)
        # Преобразуем в RGB если изображение RGBA
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

        img_array = np.array(img)
        return img_array, img.mode

    except Exception as e:
        raise ValueError(f"Ошибка загрузки изображения: {e}")


def get_image_size(img_array: np.ndarray) -> Tuple[int, int, Optional[int]]:
    """
    Получение размеров изображения

    Args:
        img_array: массив изображения

    Returns:
        Tuple[int, int, Optional[int]]: высота, ширина, количество каналов
    """
    height = img_array.shape[0]
    width = img_array.shape[1]
    channels = img_array.shape[2] if len(img_array.shape) == 3 else 1

    return height, width, channels


def add_white_noise(
    image: np.ndarray, noise_intensity: float = 0.1, seed: Optional[int] = None
) -> np.ndarray:
    """
    Наложение белого шума на изображение

    Args:
        image: исходное изображение в виде массива numpy
        noise_intensity: интенсивность шума (0.0 - 1.0)
        seed: seed для генератора случайных чисел

    Returns:
        np.ndarray: изображение с наложенным шумом
    """
    if seed is not None:
        np.random.seed(seed)

    # Нормализуем изображение к диапазону [0, 1]
    if image.dtype == np.uint8:
        image_normalized = image.astype(np.float32) / 255.0
    else:
        image_normalized = image.astype(np.float32)

    # Генерируем белый шум с нормальным распределением
    noise = np.random.normal(loc=0.0, scale=noise_intensity, size=image.shape)

    # Добавляем шум к изображению
    noisy_image = image_normalized + noise

    # Обрезаем значения до диапазона [0, 1]
    noisy_image = np.clip(noisy_image, 0.0, 1.0)

    # Конвертируем обратно в uint8 если исходное было uint8
    if image.dtype == np.uint8:
        noisy_image = (noisy_image * 255).astype(np.uint8)

    return noisy_image


def save_image(image_array: np.ndarray, output_path: str, mode: str = "RGB") -> None:
    """
    Сохранение изображения в файл

    Args:
        image_array: массив изображения
        output_path: путь для сохранения
        mode: режим цветового пространства
    """
    # Создаем директорию если ее нет
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # Конвертируем массив обратно в изображение
    img = Image.fromarray(image_array)

    # Сохраняем с сохранением формата
    if output_path.lower().endswith(".png"):
        img.save(output_path, "PNG")
    elif output_path.lower().endswith(".jpg") or output_path.lower().endswith(".jpeg"):
        img.save(output_path, "JPEG", quality=95)
    else:
        img.save(output_path)


def display_images(
    original: np.ndarray, noisy: np.ndarray, show_plots: bool = True
) -> None:
    """
    Отображение исходного и обработанного изображений

    Args:
        original: исходное изображение
        noisy: изображение с шумом
        show_plots: показывать ли графики
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Отображаем исходное изображение
    if len(original.shape) == 3:
        axes[0].imshow(original)
    else:
        axes[0].imshow(original, cmap="gray")
    axes[0].set_title("Исходное изображение")
    axes[0].axis("off")

    # Отображаем изображение с шумом
    if len(noisy.shape) == 3:
        axes[1].imshow(noisy)
    else:
        axes[1].imshow(noisy, cmap="gray")
    axes[1].set_title("Изображение с шумом")
    axes[1].axis("off")

    # Отображаем разницу
    if original.dtype == noisy.dtype:
        if original.dtype == np.uint8:
            diff = noisy.astype(np.float32) - original.astype(np.float32)
        else:
            diff = noisy - original

        # Нормализуем разницу для отображения
        diff_normalized = (diff - diff.min()) / (diff.max() - diff.min() + 1e-8)

        axes[2].imshow(diff_normalized, cmap="coolwarm")
        axes[2].set_title("Разница (увеличенная)")
        axes[2].axis("off")

    plt.tight_layout()

    if show_plots:
        plt.show()
    else:
        # Сохраняем график
        output_plot = "comparison.png"
        plt.savefig(output_plot, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"График сохранен в файл: {output_plot}")


def validate_arguments(args: argparse.Namespace) -> bool:
    """
    Валидация аргументов командной строки

    Args:
        args: аргументы командной строки

    Returns:
        bool: True если аргументы валидны, False в противном случае
    """
    # Проверка существования входного файла
    if not os.path.exists(args.input):
        print(f"Ошибка: файл {args.input} не найден")
        return False

    # Проверка интенсивности шума
    if not (0.0 <= args.noise_intensity <= 1.0):
        print("Ошибка: интенсивность шума должна быть в диапазоне от 0.0 до 1.0")
        return False

    # Проверка допустимых расширений
    valid_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"]
    _, ext = os.path.splitext(args.input.lower())
    if ext not in valid_extensions:
        print(f"Предупреждение: формат {ext} может не поддерживаться")

    return True


def print_image_info(img_array: np.ndarray, image_path: str) -> None:
    """
    Вывод информации об изображении

    Args:
        img_array: массив изображения
        image_path: путь к файлу изображения
    """
    height, width, channels = get_image_size(img_array)

    print("=" * 60)
    print("ИНФОРМАЦИЯ ОБ ИЗОБРАЖЕНИИ:")
    print(f"  Файл: {image_path}")
    print(f"  Размеры: {width} x {height} пикселей")
    print(f"  Количество каналов: {channels}")
    print(f"  Тип данных: {img_array.dtype}")
    print(f"  Диапазон значений: [{img_array.min()}, {img_array.max()}]")
    print(f"  Размер в памяти: {img_array.nbytes / 1024:.2f} KB")
    print("=" * 60)


def main() -> None:
    """
    Основная функция программы
    """
    # Парсинг аргументов
    args = parse_arguments()

    # Валидация аргументов
    if not validate_arguments(args):
        return

    try:
        # 1. Загрузка изображения
        print(f"Загрузка изображения: {args.input}")
        img_array, img_mode = load_image(args.input)

        # 2. Вывод информации о размере
        print_image_info(img_array, args.input)

        # 3. Наложение белого шума
        print("\nНаложение белого шума...")
        print(f"  Интенсивность шума: {args.noise_intensity}")
        print(f"  Seed: {args.seed if args.seed else 'не задан'}")

        noisy_image = add_white_noise(
            img_array, noise_intensity=args.noise_intensity, seed=args.seed
        )

        # 4. Сохранение результата
        print(f"\nСохранение результата: {args.output}")
        save_image(noisy_image, args.output, img_mode)

        # 5. Отображение результатов
        print("\nОтображение результатов...")
        display_images(img_array, noisy_image, args.show_plots)

        print("\n" + "=" * 60)
        print("ОПЕРАЦИЯ УСПЕШНО ЗАВЕРШЕНА!")
        print(f"  Исходный файл: {args.input}")
        print(f"  Результат сохранен: {args.output}")
        print("=" * 60)

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except ValueError as e:
        print(f"Ошибка загрузки изображения: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
