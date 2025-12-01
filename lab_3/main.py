from __future__ import annotations
import argparse
from image import load_image, save_image
from processing import apply_gradient_lightening
from visual import show_comparison

def main() -> None:
    """Основная функция программы."""
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Путь к исходному изображению")
    parser.add_argument("output", help="Путь для сохранения результата")
    parser.add_argument(
        "--direction",
        choices=["horizontal", "vertical"],
        default="horizontal",
        help="Направление градиента (по умолчанию: horizontal)",
    )
    parser.add_argument(
        "--intensity",
        type=float,
        default=1.0,
        help="Сила осветления (по умолчанию: 1.0)",
    )

    args = parser.parse_args()

    try:
        original = load_image(args.input)
        print(f"Загружено изображение: {original.shape[1]}×{original.shape[0]} пикселей")

        processed = apply_gradient_lightening(
            original, direction=args.direction, intensity=args.intensity
        )

        save_image(processed, args.output)
        print(f"Результат сохранён: {args.output}")

        show_comparison(original, processed, args.direction, args.intensity)

    except Exception as exc: 
        print(f"Ошибка: {exc}")


if __name__ == "__main__":
    main()