import argparse

import cv2

import image


def get_args() -> list[str]:
    """Parse cmd arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--source', help='Path to source image file'
    )
    parser.add_argument(
        '-o', '--output', help='Path to output image file'
    )
    parser.add_argument(
        '-v', '--is_vertical', help='Do vertical reverse need?'
    )
    args = parser.parse_args()
    if args.source is None or args.output is None:
        return None
    return [args.source, args.output, bool(args.is_vertical)]


def main() -> None:
    """Main function"""
    try:
        source, output, vertical = get_args()
        img = cv2.imread(source)
    except TypeError:
        print("Usage: python main.py -s source.jpg -o out.jpg")
        return
    except Exception as e:
        print(f"Something went wrong {e}")
        return

    print(f"Image size: {img.shape[1]}*{img.shape[0]}")
    rev_img = image.reverse_img(img.copy(), vertical)
    image.show(img, rev_img)

    try:
        cv2.imwrite(output, rev_img)
    except Exception as e:
        print(f"Something went wrong {e}")
        return


if __name__ == "__main__":
    main()
