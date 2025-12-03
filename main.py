import argparse
from __crawler__ import download_images
from __annotation__ import create_annotation
from __iterator__ import ImagePathIterator

def main():
    """Основная функция программы."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-sou", "--source", help="(google, bing, flickr, baidu)")
    parser.add_argument("-sto", "--storage-dir", help="save folder")
    parser.add_argument("-c", "--count", type=int, help="count of images")
    parser.add_argument("-a", "--annotation-file", help="path for CSV annotation")

    args = parser.parse_args()

    try:
        if args.count < 50 or args.count > 1000:
            print("Error: count must be greater than 50 and less than 100.")
            return

        download_images(args.source, args.storage_dir, args.count)
        create_annotation(args.storage_dir, args.annotation_file)

        iter = ImagePathIterator(args.annotation_file) 
        for element in iter: 
            print(element)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
