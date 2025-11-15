import argparse

from binarizer import binarize_image
from image_handler import read_image, save_image
from visualization import display_images


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
        type=int,
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
    print(f"    Filepath to the original image: '{args.input_path}'")
    print(f"    Filepath to save the processed image: '{args.output_path}'")
    print(f"    Threshold for binarization: {args.threshold}")

    try:
        original_image = read_image(args.input_path)
        binary_image = binarize_image(original_image, args.threshold)

        print(f"Resolution of original image: {original_image.shape}")

        save_image(args.output_path, binary_image)
        print(f"Image saved successfully to '{args.output_path}'")
        display_images(original_image, binary_image)

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
