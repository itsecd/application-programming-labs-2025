# ВЫПОЛНИЛ ДОЛЖИКОВ ДМИТРИЙ 6212-100503D
import argparse

import audio


def get_args() -> list[str]:
    """Parsing console arguments
    Returns None if there are no arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Path to current track",
    )
    parser.add_argument(
        "-d",
        "--dirrectory",
        type=str,
        help="Dirrectory where output file will be saved",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=str,
        help="Set window size for smoothing",
    )
    args = parser.parse_args()

    if args.file is None or args.dirrectory is None or args.size is None:
        return None
    return [args.file, args.dirrectory, args.size]


def main() -> None:
    """Entry point. The main function that demonstrates the work"""
    try:
        filename, dir, window_size = get_args()
    except TypeError:
        print("Usage python main.py -f filename -d dirrectory -s window size")
        return

    try:
        source_audio = audio.AudioTrack(filename)
        smooth_audio = audio.AudioTrack(filename)

        audio.smooth(smooth_audio, int(window_size))

        smooth_audio.filename = "smoothed_" + smooth_audio.filename
        smooth_audio.save(dir)
        source_audio.vizualize(smooth_audio)
    except ValueError:
        print("ValueError: After -s required interger")
    except FileNotFoundError:
        print("Error: File was not found on the path specified after -f")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
