import argparse

from image_processor import get_image_size, resize_image, read_image, save_image, show_image
from path_utils import get_correct_bild_path

def parser_t() -> tuple[str, str, str, int]:
    """
    Через консоль запуск кода с аргументами.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=str, help="Путь к файлу для работы с ним")
    parser.add_argument("bild", type=str, help="Путь для сохранения картинки")
    parser.add_argument("height", type=int, help="Длина")
    parser.add_argument("width", type=int, help="Ширина")
    args = parser.parse_args()
    return args.source, args.bild, args.height, args.width

def main() -> None:
    try:
        source, bild, height, width = parser_t()

        bild = get_correct_bild_path(bild)

        img = read_image(source)
        if img is None:
            return
        
        w, h = get_image_size(img)
        print(f"Исходный размер: {w} x {h}")

        if width <= 0 or height <= 0:
            raise ValueError("Длина и ширина должны быть натуральными числами")

        resized = resize_image(img, width, height)
        
        w_new, h_new = get_image_size(resized)
        print(f"Новый размер: {w_new} x {h_new}")

        show_image(img, resized)

        save_image(resized, bild)
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
