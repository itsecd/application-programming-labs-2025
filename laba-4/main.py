import argparse

import csv_utility


def parse_arguments() -> argparse.Namespace:
    """
    Adds and parses command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Tool to analyze data from CSV annotation.")
    parser.add_argument(
        '--annotation_path',
        '-a',
        required=True,
        help='Filepath to the original CSV annotation.'
    )
    parser.add_argument(
        '--output_csv_path',
        '-o',
        default='analysis_results.csv',
        help='Filepath to save the DataFrame in CSV.'
    )
    parser.add_argument(
        '--output_plot_path',
        default='brightness_histogram.png',
        help='Filepath to save the histogram.'
    )
    return parser.parse_args()


def main() -> None:
    """
    Main function.
    """
    args = parse_arguments()

    print("Args for script:")
    print(f"    Filepath to the original CSV annotation: '{args.annotation_path}'")
    print(f"    Filepath to save the DataFrame in CSV: '{args.output_csv_path}'")
    print(f"    Filepath to save the histogram: '{args.output_plot_path}'")

    try:
        dataframe = csv_utility.load_and_enrich_data(args.annotation_path)

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
