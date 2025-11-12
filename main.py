import argparse

import cv2
import matplotlib.pyplot as plt
import numpy as np


def reverse_img(img: np.ndarray) -> np.ndarray:
    """Reverse image row by row"""
    n, m = img.shape[0], img.shape[1]
    for i in range(n):
        img[i] = img[i][::-1]
    return img


def get_args() -> list[str]:
    """Parse cmd arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--source', help='Path to source image file'
    )
    parser.add_argument(
        '-o', '--output', help='Path to output image file'
    )
    args = parser.parse_args()
    if args.source is None or args.output is None:
        return None
    return [args.source, args.output]


def show(img, rev_img) -> None:
    """Show source and reversed image"""

    fig, axes = plt.subplots(1, 2)
    axes[0].imshow(img)
    axes[1].imshow(rev_img)

    axes[0].set_title("Source")
    axes[1].set_title("Result")

    plt.show()


def main() -> None:
    """Main function"""
    try:
        source, output = get_args()
        img = cv2.imread(source)
    except TypeError:
        print("Usage: python main.py -s source.jpg -o out.jpg")
        return
    except Exception as e:
        print(f"Something went wrong {e}")
        return

    print(f"Image size: {img.shape[1]}*{img.shape[0]}")
    rev_img = reverse_img(img.copy())
    show(img, rev_img)

    try:
        cv2.imwrite(output, rev_img)
    except Exception as e:
        print(f"Something went wrong {e}")
        return


if __name__ == "__main__":
    main()
