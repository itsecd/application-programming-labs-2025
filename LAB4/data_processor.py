import pandas as pd
from typing import List, Optional
from file_processor import calculate_brightness_range, create_brightness_range_category


def create_dataframe(absolute_paths: List[str], relative_paths: List[str]) -> pd.DataFrame:
    """
    Создает DataFrame с путями и вычисляет диапазоны яркости
    
    Args:
        absolute_paths: Список абсолютных путей
        relative_paths: Список относительных путей
        
    Returns:
        DataFrame с данными об изображениях
    """
    df = pd.DataFrame({
        'absolute_file_path': absolute_paths,
        'relative_file_path': relative_paths
    })
    
    # Добавляем колонку с максимальным диапазоном яркости
    df['max_brightness_range'] = [calculate_brightness_range(path) for path in df['absolute_file_path']]
    
    # Добавляем колонку с категорией диапазона
    df['brightness_range_category'] = df['max_brightness_range'].apply(create_brightness_range_category)
    
    return df


def sort_dataframe(df: pd.DataFrame, column: str = 'brightness_range_category', ascending: bool = True) -> pd.DataFrame:
    """
    Функция сортировки DataFrame по категории диапазона
    
    Args:
        df: DataFrame для сортировки
        column: Колонка для сортировки
        ascending: Порядок сортировки
        
    Returns:
        Отсортированный DataFrame
    """
    # Создаем порядок сортировки для категорий
    category_order = ["0-50", "51-100", "101-150", "151-200", "201-255"]
    df['sort_order'] = df[column].apply(lambda x: category_order.index(x))
    df_sorted = df.sort_values('sort_order', ascending=ascending)
    return df_sorted.drop('sort_order', axis=1)


def filter_dataframe(df: pd.DataFrame, column: str = 'brightness_range_category', value: str = '101-150') -> pd.DataFrame:
    """
    Функция фильтрации DataFrame
    
    Args:
        df: DataFrame для фильтрации
        column: Колонка для фильтрации
        value: Значение для фильтрации
        
    Returns:
        Отфильтрованный DataFrame
    """
    return df[df[column] == value]


def get_dataframe_info(df_sorted: pd.DataFrame, filtered_df: pd.DataFrame) -> None:
    """
    Выводит информацию о DataFrame
    
    Args:
        df_sorted: Отсортированный DataFrame
        filtered_df: Отфильтрованный DataFrame
    """
    print(f"Всего изображений: {len(df_sorted)}")
    print(f"Колонки: {list(df_sorted.columns)}")
    print("\nРаспределение по категориям яркости:")
    print(df_sorted['brightness_range_category'].value_counts().sort_index())
    
    print(f"\nФильтрация по категории '101-150': найдено {len(filtered_df)} файлов")