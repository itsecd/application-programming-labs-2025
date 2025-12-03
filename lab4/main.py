import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import sys
from typing import Optional, Tuple


def read_annotation(file_path: str) -> pd.DataFrame:
    """Читает файл аннотации из CSV файла с разделителем ';'."""
    try:
        df = pd.read_csv(file_path, sep=';', header=None, 
                        names=['absolute_path', 'relative_path'])
        return df
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден", file=sys.stderr)
        sys.exit(1)


def determine_orientation(image_path: str) -> Optional[str]:
    """Определяет ориентацию изображения по пути."""
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            if width == height:
                return 'квадратное'
            elif width > height:
                return 'горизонтальное'
            else:
                return 'вертикальное'
    except Exception:
        return None


def add_orientation_column(df: pd.DataFrame) -> pd.DataFrame:
    """Добавляет колонку с ориентацией изображений в DataFrame."""
    df_copy = df.copy()
    df_copy['orientation'] = df_copy['absolute_path'].apply(determine_orientation)
    df_copy = df_copy.dropna(subset=['orientation'])
    return df_copy


def sort_by_orientation(df: pd.DataFrame, ascending: bool = True) -> pd.DataFrame:
    """Сортирует DataFrame по ориентации изображений."""
    order = {'горизонтальное': 0, 'квадратное': 1, 'вертикальное': 2}
    df_copy = df.copy()
    df_copy['orientation_order'] = df_copy['orientation'].map(order)
    df_copy = df_copy.sort_values('orientation_order', ascending=ascending)
    df_copy = df_copy.drop(columns=['orientation_order'])
    return df_copy


def filter_by_orientation(df: pd.DataFrame, orientation: str) -> pd.DataFrame:
    """Фильтрует DataFrame по заданной ориентации."""
    return df[df['orientation'] == orientation].copy()


def create_histogram(df: pd.DataFrame, save_path: str = 'orientation_histogram.png') -> None:
    """Создает гистограмму распределения ориентаций изображений."""
    orientation_counts = df['orientation'].value_counts()
    
    plt.figure(figsize=(8, 5))
    colors = {'горизонтальное': 'skyblue', 'квадратное': 'lightgreen', 'вертикальное': 'lightcoral'}
    
    bars = plt.bar(
        orientation_counts.index,
        orientation_counts.values,
        color=[colors.get(ori, 'gray') for ori in orientation_counts.index],
        edgecolor='black'
    )
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height, f'{int(height)}', 
                ha='center', va='bottom', fontweight='bold')
    
    plt.title('Распределение ориентаций изображений')
    plt.xlabel('Ориентация')
    plt.ylabel('Количество изображений')
    plt.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    

def save_results(df: pd.DataFrame, file_path: str) -> None:
    """Сохраняет DataFrame с результатами в CSV файл."""
    df.to_csv(file_path, sep=';', index=False, encoding='utf-8')


def display_statistics(df: pd.DataFrame) -> None:
    """Выводит статистику по данным."""
    print(f"Всего изображений: {len(df)}")
    
    orientation_counts = df['orientation'].value_counts()
    print("\nРаспределение ориентаций:")
    for orientation, count in orientation_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {orientation}: {count} ({percentage:.1f}%)")


def main() -> None:
    """Основная функция для выполнения лабораторной работы."""
    print("Лабораторная работа №4, вариант 10")
    print("Анализ ориентации изображений")
    print("=" * 50)
    
    try:
        df = read_annotation('annotation.csv')
        print(f"Загружено {len(df)} записей из файла аннотации")
        
        df = add_orientation_column(df)
        print(f"Обработано {len(df)} изображений")
        
        display_statistics(df)
        
        sorted_df = sort_by_orientation(df, ascending=True)
        print("\nДанные отсортированы по ориентации")
        
        create_histogram(sorted_df, 'orientation_histogram.png')
        print("Гистограмма сохранена как 'orientation_histogram.png'")
        
        # Сохранение результатов
        save_results(sorted_df, 'lab4_results.csv')
        print("Результаты сохранены в 'lab4_results.csv'")
        
        # Вывод первых строк
        print("\nПервые 5 строк обработанных данных:")
        print(sorted_df.head())
        
        print(f"\nЛабораторная работа успешно завершена!")
        
    except Exception as e:
        print(f"Произошла ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()