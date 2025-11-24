import argparse

import pandas as pd

import funcs


def get_args() -> list[str]:
    """Parsing console arguments
    Returns None if there are no arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--file",
        type=str,
        help="Path to file.csv",
    )
    parser.add_argument(
        "-o",
        "--out_file",
        type=str,
        help="Path to out_file.csv",
    )
    args = parser.parse_args()

    if args.file is None or args.out_file is None:
        return None
    return [args.file, args.out_file]


def main() -> None:
    """Main function"""

    try:
        csv, out = get_args()
    except TypeError:
        print("Usage: python main.py -c file.csv -o out_file.csv")
        return
    try:
        df = pd.read_csv(csv)
    except:
        print(f"Error: Cannot to read {csv}")
        return

    df['dominant_color'] = df["Relative Path"].apply(funcs.get_dominant_color)
    df['brightness_range'] = df['dominant_color'].apply(funcs.get_brightness_range)

    df_sort = funcs.sort_by_column(df, "brightness_range")

    funcs.show_and_save(df_sort)

    try:
        df.to_csv(out, index=False)
    except:
        print("Cannot to save dataframe")


if __name__ == "__main__":
    main()
