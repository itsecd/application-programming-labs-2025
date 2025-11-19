import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image


def get_dominant_color(image_path: str) -> list[int]:
    """Calculate dominant color as average every chanels"""
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        pixels = np.array(img)
        r_mean = pixels[:, :, 0].mean()  # красный канал
        g_mean = pixels[:, :, 1].mean()  # зеленый канал
        b_mean = pixels[:, :, 2].mean()  # синий канал

    return [int(r_mean), int(g_mean), int(b_mean)]


def get_brightness_range(rgb: list[int]) -> str:
    """Calculate brightness for vizualize distribution"""
    brightness = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
    range_start = (brightness // 50) * 50
    return f"{int(range_start)}-{int(range_start + 49)}"


def sort_by_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Sorting DataFrame by column"""
    return df.sort_values(by=column)


def filter_by_range(df: pd.DataFrame, range_str: str) -> pd.DataFrame:
    """Filter DataFrame by brightness range"""
    return df[df['Brightness Range'] == range_str]


def show_and_save(df_sort: pd.DataFrame) -> None:
    """Show and save hystogramm of distribution brightness dominant color"""
    range_counts = df_sort['Brightness Range'].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    plt.bar(range_counts.index, range_counts.values, color='skyblue')
    plt.xlabel('Диапазоны яркости доминирующего цвета')
    plt.ylabel('Количество файлов')
    plt.title('Распределение картинок по диапазонам яркости доминирующего цвета')
    plt.tight_layout()
    plt.savefig("image_color_hyst.png")
    plt.show()
