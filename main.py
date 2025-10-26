# ВЫПОЛНИЛ ДОЛЖИКОВ ДМИТРИЙ 6212-100503D ВАРИАНТ 29
import argparse

import audio


def get_args() -> list[str]:
    """Parsing console arguments
    Returns None if there are no arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--dirrectory",
        type=str,
        help="Set current dirrectory to download",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Set .csv filename",
    )
    parser.add_argument(
        "-c",
        "--count",
        type=str,
        help="Set how many tracks will be download",
    )
    args = parser.parse_args()

    if args.file is None or args.dirrectory is None or args.count is None:
        return None
    return [args.file, args.dirrectory, args.count]


def main() -> None:
    try:
        filename, dir, count = get_args()
    except TypeError:
        print("Usage python main.py -f filename -d dirrectory -c count")
        return
    filename = filename + ".csv"
    audio_parser = audio.AudioParser(dir, filename)
    try:
        audio_parser.download_audios(int(count))
    except ValueError:
        print("ValueError: After -c required an integer")
    audio_parser.create_annotation()

    print("\nIteration in CSV:")
    for audio_path in audio.AudioIterator(filename):
        print(audio_path)

    print("\nIteration in dirrectory:")
    for audio_path in audio.AudioIterator(dir):
        print(audio_path)


if __name__ == "__main__":
    main()
