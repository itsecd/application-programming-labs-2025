import pandas as pd
from pathlib import Path
from PIL import Image
from typing import Optional, Tuple, List


def load_dataframe_from_csv(csv_path: str) -> pd.DataFrame:
    """
    Загружает DataFrame из CSV файла аннотации.
    """
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"Файл {csv_path} не найден")
    
    print(f"Загрузка данных из: {csv_path}")
    df = pd.read_csv(csv_path)
    
    # Переименовываем колонки для лучшей читаемости
    df = df.rename(columns={
        'absolute_path': 'Абсолютный путь',
        'relative_path': 'Относительный путь',
        'filename': 'Имя файла'
    })
    
    print(f"Загружено записей: {len(df)}")
    return df


def get_image_dimensions(image_path: str) -> Optional[Tuple[int, int]]:
    """
    Получает размеры изображения.
    """
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception as e:
        print(f"Ошибка при обработке {image_path}: {e}")
        return None


def add_image_width_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавляет колонку с шириной (длиной) каждого изображения.
    """
    print("\nДобавление колонки с шириной изображений...")
    widths: List[Optional[int]] = []
    
    for idx, row in df.iterrows():
        dimensions = get_image_dimensions(row['Абсолютный путь'])
        if dimensions:
            widths.append(dimensions[0])  # ширина
        else:
            widths.append(None)
        
        if (idx + 1) % 10 == 0:
            print(f"Обработано: {idx + 1}/{len(df)}")
    
    df['Ширина изображения'] = widths
    
    # Удаляем строки с ошибками
    initial_count = len(df)
    df = df.dropna(subset=['Ширина изображения'])
    df['Ширина изображения'] = df['Ширина изображения'].astype(int)
    
    removed_count = initial_count - len(df)
    if removed_count > 0:
        print(f"Удалено записей с ошибками: {removed_count}")
    
    print(f"Колонка добавлена. Валидных записей: {len(df)}")
    
    return df


def sort_by_width(df: pd.DataFrame, ascending: bool = True) -> pd.DataFrame:
    """
    Сортирует DataFrame по ширине изображения.
    """
    order = "возрастанию" if ascending else "убыванию"
    print(f"\nСортировка по {order} ширины...")
    
    sorted_df = df.sort_values(
        by='Ширина изображения', 
        ascending=ascending
    ).reset_index(drop=True)
    
    print("Первые 5 записей после сортировки:")
    print(sorted_df[['Имя файла', 'Ширина изображения']].head())
    
    return sorted_df


def filter_by_width(
    df: pd.DataFrame, 
    min_width: Optional[int] = None, 
    max_width: Optional[int] = None
) -> pd.DataFrame:
    """
    Фильтрует DataFrame по ширине изображения.
    """
    print(f"\nФильтрация по ширине...")
    original_count = len(df)
    
    filtered_df = df.copy()
    
    if min_width is not None:
        filtered_df = filtered_df[filtered_df['Ширина изображения'] >= min_width]
        print(f"Минимальная ширина: {min_width} px")
    
    if max_width is not None:
        filtered_df = filtered_df[filtered_df['Ширина изображения'] <= max_width]
        print(f"Максимальная ширина: {max_width} px")
    
    filtered_count = len(filtered_df)
    print(f"Записей до фильтрации: {original_count}")
    print(f"Записей после фильтрации: {filtered_count}")
    print(f"Отфильтровано: {original_count - filtered_count}")
    
    return filtered_df


def save_dataframe(df: pd.DataFrame, output_path: str) -> None:
    """
    Сохраняет DataFrame в CSV файл.
    """
    try:
        # Создаем директорию, если её нет
        output_dir = Path(output_path).parent
        if output_dir != Path('.'):
            output_dir.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"DataFrame сохранен в: {output_path}")
    except Exception as e:
        raise IOError(f"Ошибка при сохранении DataFrame: {e}")