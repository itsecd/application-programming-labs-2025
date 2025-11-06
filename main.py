import argparse
import pandas as pd

import functions


def get_args() -> list[str]:
    """Parsing console arguments
    Returns None if there are no arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Path to .csv file",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=str,
        help="Set threshold for samples",
    )
    parser.add_argument(
        "-r",
        "--res",
        type=str,
        help="Path, where result.csv file will be saved",
    )
    args = parser.parse_args()

    if args.file is None or args.threshold is None or args.file is None:
        return None
    return [args.file, args.threshold, args.res]


def main() -> None:
    """Entry point. Main function"""

    try:
        file, threshold, res = get_args()
    except:
        print("Usage: python main.py -f file.csv -t threshold -r res_filename.csv")
        return
    try:
        df = pd.read_csv(file)
    except:
        print(f"Error: Cannot to read {file}")
        return

    paths = list(df["Relative Path"])

    tracks = list(functions.AudioTrack(path).get_samples() for path in paths)
    try:
        ratios = list(
            functions.calculate_ratio(track, float(threshold)) for track in tracks
        )
    except ValueError:
        print("After -t required float")
        return

    df["Ratio below threshold"] = ratios

    df = functions.sort_by_ratio(df)
    functions.visualization(df)
    try:
        df.to_csv(res, index=False)
    except:
        print("Cannot to save dataframe")


if __name__ == "__main__":
    main()
