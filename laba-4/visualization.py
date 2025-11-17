import matplotlib.pyplot as plt
import pandas as pd


def plot_histogram(df: pd.DataFrame, output_plot_path: str) -> None:
    """
    Plots and saves histogram of the distribution of image brightness.
    :param df: DataFrame to make histogram of.
    :param output_plot_path: Filepath to save the histogram.
    """
    ranges = df['brightness_range'].value_counts().sort_index()

    plt.figure(figsize=(11, 8))
    ranges.plot(kind='bar')

    plt.title('Histogram of the distribution of image brightness')
    plt.xlabel('Range of brightness (0-255)')
    plt.ylabel('Number of images')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()

    try:
        plt.savefig(output_plot_path)
    except Exception as e:
        print(f"Error while saving histogram to {output_plot_path} : {e}")

    plt.show()
