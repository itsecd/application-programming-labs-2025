from image import read_image, give_image_info, save_image
from parser import parse_args
from transformation import to_grayscale, show_pair
import sys

def main():
    args = parse_args()

    try:
        img = read_image(args.input)

        shape = give_image_info(img)
        print(f"Размер исходного файла: {shape[1]}×{shape[0]}")

        gray = to_grayscale(img)

        show_pair(img, gray)

        save_image(args.output, gray)
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()