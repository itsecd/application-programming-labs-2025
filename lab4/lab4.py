import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import os
from typing import Optional, Tuple, List


def read_annotation_data(file_path: str) -> pd.DataFrame:
    """
    Читает данные аннотации из CSV файла.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Успешно загружено {len(df)} записей из {file_path}")
        return df
    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
        raise
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {str(e)}")
        raise


def rename_dataframe_columns(df: pd.DataFrame, column_mapping: dict) -> pd.DataFrame:
    """
    Переименовывает колонки DataFrame.
    """
    df_renamed = df.rename(columns=column_mapping)
    print("Колонки успешно переименованы")
    return df_renamed


def get_image_width(image_path: str) -> Optional[int]:
    """
    Получает ширину изображения.
    """
    try:
        with Image.open(image_path) as img:
            return img.size[0]
    except Exception as e:
        print(f"Ошибка при обработке {image_path}: {str(e)}")
        return None


def add_width_column(df: pd.DataFrame, path_column: str = 'relative_path') -> pd.DataFrame:
    """
    Добавляет колонку с шириной изображения в DataFrame.
    """
    df_copy = df.copy()
    df_copy['width'] = df_copy[path_column].apply(get_image_width)
    
    # Удаляем строки, где не удалось получить ширину
    initial_count = len(df_copy)
    df_copy = df_copy.dropna(subset=['width'])
    removed_count = initial_count - len(df_copy)
    
    if removed_count > 0:
        print(f"Удалено {removed_count} записей с некорректными изображениями")
    
    print(f"Добавлена колонка 'width' для {len(df_copy)} изображений")
    return df_copy


def sort_by_width(df: pd.DataFrame, ascending: bool = True) -> pd.DataFrame:
    """
    Сортирует DataFrame по ширине изображения.
    """
    sorted_df = df.sort_values('width', ascending=ascending)
    order = "возрастанию" if ascending else "убыванию"
    print(f"Данные отсортированы по {order} ширины")
    return sorted_df


def filter_by_width(df: pd.DataFrame, min_width: Optional[int] = None, 
                   max_width: Optional[int] = None) -> pd.DataFrame:
    """
    Фильтрует DataFrame по ширине изображения.
    """
    filtered_df = df.copy()
    
    if min_width is not None:
        filtered_df = filtered_df[filtered_df['width'] >= min_width]
        print(f"Применен фильтр: ширина >= {min_width}")
    
    if max_width is not None:
        filtered_df = filtered_df[filtered_df['width'] <= max_width]
        print(f"Применен фильтр: ширина <= {max_width}")
    
    print(f"После фильтрации осталось {len(filtered_df)} записей")
    return filtered_df


def create_width_plot(df: pd.DataFrame, save_path: str = 'width_plot.png') -> None:
    """
    Создает график зависимости ширины изображения от номера в отсортированном списке.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(df)), df['width'], marker='o', linestyle='-', 
             markersize=4, linewidth=1, alpha=0.7)
    
    plt.title('Зависимость ширины изображения от номера в отсортированном списке', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Номер изображения в отсортированном списке', fontsize=12)
    plt.ylabel('Ширина изображения (пиксели)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Добавляем информацию о данных в легенду
    min_width = df['width'].min()
    max_width = df['width'].max()
    avg_width = df['width'].mean()
    plt.text(0.02, 0.98, f'Минимум: {min_width} px\nМаксимум: {max_width} px\nСреднее: {avg_width:.1f} px', 
             transform=plt.gca().transAxes, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"График сохранен как {save_path}")


def save_dataframe(df: pd.DataFrame, file_path: str) -> None:
    """
    Сохраняет DataFrame в CSV файл.
    """
    try:
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"DataFrame успешно сохранен в {file_path}")
    except Exception as e:
        print(f"Ошибка при сохранении DataFrame: {str(e)}")
        raise


def display_dataframe_info(df: pd.DataFrame, title: str = "Информация о данных") -> None:
    """
    Выводит основную информацию о DataFrame.
    """
    print(f"\n{'='*50}")
    print(title)
    print(f"{'='*50}")
    print(f"Количество записей: {len(df)}")
    print(f"Колонки: {list(df.columns)}")
    if 'width' in df.columns:
        print(f"Статистика по ширине:")
        print(f"  Минимум: {df['width'].min()} px")
        print(f"  Максимум: {df['width'].max()} px")
        print(f"  Среднее: {df['width'].mean():.1f} px")
        print(f"  Медиана: {df['width'].median()} px")
    print(f"{'='*50}\n")


def main() -> None:
    """
    Основная функция для выполнения лабораторной работы №4.
    """
    print("Лабораторная работа №4: Анализ и визуализация данных")
    print("=" * 60)
    
    try:
        # 1. Чтение данных из CSV файла
        df = read_annotation_data('annotation.csv')
        
        # 2. Переименование колонок
        column_mapping = {
            'Абсолютный путь': 'absolute_path',
            'Относительный путь': 'relative_path'
        }
        df = rename_dataframe_columns(df, column_mapping)
        
        # 3. Добавление колонки с шириной изображения
        df = add_width_column(df, 'relative_path')
        
        # Вывод информации о данных до обработки
        display_dataframe_info(df, "Данные после добавления ширины")
        
        # 4. Сортировка данных по ширине (по возрастанию)
        sorted_df = sort_by_width(df, ascending=True)
        
        # 5. Демонстрация фильтрации
        filtered_df = filter_by_width(sorted_df, min_width=500)
        
        # 6. Создание и сохранение графика
        create_width_plot(sorted_df, 'width_plot.png')
        
        # 7. Сохранение результатов
        save_dataframe(sorted_df, 'lab4_results.csv')
        
        # Вывод первых строк обработанных данных
        print("\nПервые 5 строк обработанных данных:")
        print(sorted_df.head())
        
        print("\nЛабораторная работа успешно завершена!")
        
    except Exception as e:
        print(f"Произошла ошибка при выполнении программы: {str(e)}")
        return


if __name__ == "__main__":
    main()