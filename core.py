import pandas as pd
from PIL import Image
from typing import Optional, Tuple, List


def load_dataframe_from_csv(csv_path: str) -> pd.DataFrame:
    """
    Загружает DataFrame из CSV файла.
    """
    
    df = pd.read_csv(csv_path)
    return df


def get_image_dimensions(image_path: str) -> Optional[Tuple[int, int]]:
    """
    Получает размеры изображения (ширину и высоту).
    """
    
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception:
        return None


def add_image_width_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавляет колонку с шириной изображения в DataFrame.
    """
    
    widths: List[Optional[int]] = []

    for idx, row in df.iterrows():
        dimensions = get_image_dimensions(row['absolute_path'])
        if dimensions:
            widths.append(dimensions[0])
        else:
            widths.append(None)

    df['image_width'] = widths
    df = df.dropna(subset=['image_width'])
    df['image_width'] = df['image_width'].astype(int)

    return df


def save_dataframe(df: pd.DataFrame, output_path: str) -> None:
    """
    Сохраняет DataFrame в CSV файл.
    """

    df.to_csv(output_path, index=False, encoding='utf-8')