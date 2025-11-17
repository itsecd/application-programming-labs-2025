import cv2
import numpy as np
import pandas as pd

BRIGHTNESS_LABELS = ["0-31", "32-63", "64-95", "96-127", "128-159", "160-191", "192-223", "224-255"]


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
        print(f"Can't get image at: {absolute_path} : {e}")
    return np.nan


def load_and_enrich_data(annotation_path: str) -> pd.DataFrame:
    """
    Load CSV, add titles and new column with brightness to DataFrame.
    :param annotation_path: Filepath to the original CSV annotation.
    :return: DataFrame.
    """
    try:
        df = pd.read_csv(annotation_path, header=None)
    except FileNotFoundError:
        raise FileNotFoundError(f"Can't found file at: {annotation_path}")

    df.columns = ['absolute_path', 'relative_path']

    df['brightness'] = df['absolute_path'].apply(get_image_brightness)

    df.dropna(subset=['brightness'], inplace=True)

    # right=False -> [0,32), ...
    bins = [0, 32, 64, 96, 128, 160, 192, 224, 256]
    df['brightness_range'] = pd.cut(df['brightness'], bins=bins, labels=BRIGHTNESS_LABELS, right=False)

    return df


def save_data(df_to_save: pd.DataFrame, output_csv_path: str) -> None:
    """
    Saves DataFrame to a CSV.
    :param df_to_save: DataFrame to save.
    :param output_csv_path: Filepath to save the DataFrame in CSV.
    """
    df_to_save.to_csv(output_csv_path, index=False)
