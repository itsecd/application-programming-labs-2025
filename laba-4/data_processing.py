import cv2
import numpy as np
import pandas as pd


def get_image_brightness(absolute_path: str) -> float:
    """
    Return the average brightness value of the image across all channels.
    :param absolute_path: Absolute path of the analyzed image.
    :return: The average brightness value of the image.
    """
    try:
        image = cv2.imread(absolute_path)
        if image is not None:
            return image.mean()
    except Exception as e:
        raise Exception(f"Can't get image at: {absolute_path} : {e}")
    return np.nan


def load_data(annotation_path: str) -> pd.DataFrame:
    """
    Load CSV, add titles.
    :param annotation_path: Filepath to the original CSV annotation.
    :return: DataFrame.
    """
    try:
        df = pd.read_csv(annotation_path, header=None)
    except FileNotFoundError:
        raise FileNotFoundError(f"Can't found file at: {annotation_path}")

    df.columns = ['absolute_path', 'relative_path']

    return df


def enrich_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    And new column with brightness to DataFrame.
    :param df: DataFrame to edit.
    :return: DataFrame.
    """
    df['brightness'] = df['absolute_path'].apply(get_image_brightness)
    df.dropna(subset=['brightness'], inplace=True)

    return df


def add_range(df: pd.DataFrame, bins: list[int]) -> pd.DataFrame:
    """
    And new column with brightness to DataFrame.
    :param df: DataFrame to edit.
    :param bins: List of integers with ranges for brightness.
    :return: DataFrame.
    """
    # right=False -> [0,32), ...

    labels = []
    for i in range(len(bins) - 1):
        labels.append(f"{bins[i]}-{bins[i + 1] - 1}")

    df['brightness_range'] = pd.cut(df['brightness'], bins=bins, labels=labels, right=False)

    return df


def save_data(df_to_save: pd.DataFrame, output_csv_path: str) -> None:
    """
    Saves DataFrame to a CSV.
    :param df_to_save: DataFrame to save.
    :param output_csv_path: Filepath to save the DataFrame in CSV.
    """
    # df_final = df_to_save['absolute_path', 'relative_path', 'brightness_range']
    df_to_save.to_csv(output_csv_path, index=False)
