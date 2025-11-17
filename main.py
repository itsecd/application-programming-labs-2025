import argparse

import image


def get_args() -> list[str]:
    """Parse cmd arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--directory", help="Directory where image will be saved")
    parser.add_argument("-f", "--annotation_file", help="Filename annotation csv file")
    parser.add_argument(
        "-d", "--date_range", help="Date range (format YYYY-MM-DD-YYYY-MM-DD)"
    )
    parser.add_argument("-c", "--count", help="How many images will be download")
    parser.add_argument(
        "-l", "--list", nargs="*", help="Set keywords for image download"
    )
    args = parser.parse_args()
    if (
        args.directory is None
        or args.annotation_file is None
        or args.date_range is None
        or args.count is None
    ):
        return None
    return [
        args.directory,
        args.annotation_file,
        args.date_range,
        args.count,
        args.list,
    ]


def main() -> None:
    """Main function"""
    try:
        directory, annotation_file, date_range, count, keywords = get_args()
        # python main.py -o res -f data.csv -d 2001-01-01-2023-05-05 -c 52 -l [keywords]
        start, end = image.parse_date_range(date_range)
    except TypeError:
        print(
            "Usage: python main.py -o download_dir -f data.csv -d YYYY-MM-DD-YYYY-MM-DD -c count of images (-l [keywords] optional)"
        )
        return
    except Exception as e:
        print(f"Something went wrong: {e}")
        return
    if keywords is None:
        image_paths = image.download_horse_images(start, end, directory, int(count))
    else:
        image_paths = image.download_horse_images(
            start, end, directory, int(count), keywords
        )

    print(f"\nDownloaded {len(image_paths)} images")

    image.create_annotation_csv(image_paths, annotation_file, directory)

    iterator = image.ImageIterator(annotation_file)

    for path in iterator:
        print(path)


if __name__ == "__main__":
    main()
