from __future__ import annotations

from blend import alpha_blend
from cli import parse_args
from io_utils import ImageReadError, read_image, save_image
from viz import print_sizes, show_images


def main() -> None:
    """Основная логика программы."""
    args = parse_args()
    try:
        img1 = read_image(args.img1)
        img2 = read_image(args.img2)
        print_sizes(img1, img2)

        result = alpha_blend(img1, img2, alpha=args.alpha)

        show_images(img1, img2, result)
        save_image(args.out, result)
        print(f"Готово. Результат: {args.out}")
    except ImageReadError as exc:
        print(f"[Ошибка чтения] {exc}")
    except ValueError as exc:
        print(f"[Неверные параметры] {exc}")
    except Exception as exc:  # noqa: BLE001
        print(f"[Неожиданная ошибка] {exc}")


if __name__ == "__main__":
    main()