import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def get_channel_brightness(image_path: str) -> tuple[int, int, int]:
    """Эта функция получает средние значения яркости по каналам"""
    img = cv2.imread(image_path)
    
    if img is None:
        raise FileNotFoundError("Image not found")

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    r_avg = np.mean(img_rgb[:, :, 0])
    g_avg = np.mean(img_rgb[:, :, 1])
    b_avg = np.mean(img_rgb[:, :, 2])

    return (r_avg, g_avg, b_avg)


def filtered_by_columns(df: pd.DataFrame, 
                        r_avg_min: float,
                        g_avg_min: float, 
                        b_avg_min: float) -> pd.DataFrame:
    "Данная функция фильтрует DataFrame по минимальным значениям r_avg, g_avg, b_avg"
    df_filtered = df.copy()

    mask = (df_filtered['r_avg'] >= r_avg_min) & (df_filtered['g_avg'] >= g_avg_min) & (df_filtered['b_avg'] >= b_avg_min)

    return df_filtered[mask].reset_index(drop=True)


def add_brightness_columns(df: pd.DataFrame) -> None:
    """Эта функция добавляет  колонки со средними значениями яркости по каждому каналу (r, g, b) изображения"""
    df['r_avg'] = None
    df['g_avg'] = None
    df['b_avg'] = None

    for i in range(0, len(df)):
        r_avg, g_avg, b_avg = get_channel_brightness(df['absolute_path'][i])
        df.loc[i, 'r_avg'] = r_avg
        df.loc[i, 'g_avg'] = g_avg
        df.loc[i, 'b_avg'] = b_avg
        

def sort_by_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Данная функция возвращает отсортированный по столбцам DataFrame"""
    return df.sort_values(by=['r_avg', 'g_avg', 'b_avg']).reset_index(drop=True)


def save_data_frame(path_to_dir: str, filename: str, df: pd.DataFrame) -> None:
    pass


def main() -> None: 
    df = pd.read_csv("annotation.csv")
    df.columns = ["absolute_path", "relative_path"]
    add_brightness_columns(df)
    print(df)
    df = sort_by_columns(df)
    print(filtered_by_columns(df, 110, 131, 11))
    

if __name__ == "__main__":
    main()