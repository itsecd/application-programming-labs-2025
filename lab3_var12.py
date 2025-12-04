import argparse
import traceback

from image_operations import (
    load_image,
    save_image,
    add_white_noise,
    display_images,
    print_image_info,
    validate_arguments,
)


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

    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

        traceback.print_exc()


if __name__ == "__main__":
    main()
