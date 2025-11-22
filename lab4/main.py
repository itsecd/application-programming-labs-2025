import pandas as pd


def main() -> None:
    args = parse_args()

    try:
        download_images(args.output, args.keywords)
        create_annotation(args.output, args.annotation)
        files_iterator = FileIterator(args.annotation)
           
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
       