import argparse

import cv2

from binarizer import binarize_image


def parse_arguments() -> argparse.Namespace:
    """
    Adds and parses command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Web scraper for downloading snake images by color.")
    parser.add_argument(
        '--input_path',
        '-i',
        required=True,
        help='Filepath to the original image.'
    )
    parser.add_argument(
        '--output_path',
        '-o',
        required=True,
        help='Filepath to save the processed image.'
    )
    parser.add_argument(
        '--threshold',
        '-t',
        default=127,
        help='Threshold for binarization (0-255). Default 127.'
    )
    return parser.parse_args()


def main() -> None:
    """
    Main function.
    """
    args = parse_arguments()

    print("Args for script:")
    print(f"    Filepath to the original image: {args.input_path}")
    print(f"    Filepath to save the processed image: {args.output_path}")
    print(f"    Threshold for binarization: {args.threshold}")

    try:
        binary_image = binarize_image(args.input_path, args.threshold)
        original_image = cv2.imread(args.input_path)
        print(f"Resolution of original image: {original_image.shape}")
        print(f"Resolution of binary image: {binary_image.shape}")


    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()