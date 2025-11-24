import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_audio_dataframe(csv_path):
    """Создает DataFrame с путями к аудиофайлам из CSV аннотации."""
    df = pd.read_csv(csv_path)
    audio_df = df[['absolute_path', 'relative_path']].copy()
    audio_df.columns = ['audio_absolute_path', 'audio_relative_path']
    
    return audio_df


def add_mock_duration_column(df):
    """Добавляет колонку с длительностью аудиофайлов."""
    np.random.seed(42) 
    durations = np.random.uniform(3, 45, len(df))
    durations = np.sort(durations)
    durations += np.random.normal(0, 5, len(df))
    durations = np.clip(durations, 2, 50) 
    
    df['audio_duration_seconds'] = durations
    return df


def sort_by_duration(df, ascending=True):
    """Сортирует DataFrame по длительности аудиофайлов."""
    return df.sort_values('audio_duration_seconds', ascending=ascending)


def filter_by_duration(df, min_duration=0, max_duration=None):
    """Фильтрует DataFrame по длительности аудиофайлов."""
    filtered_df = df[df['audio_duration_seconds'] >= min_duration]
    
    if max_duration is not None:
        filtered_df = filtered_df[filtered_df['audio_duration_seconds'] <= max_duration]
    
    return filtered_df


def plot_durations(df, output_plot):
    """Строит график длительностей аудиофайлов."""
    plt.figure(figsize=(14, 8))
    
    sorted_df = sort_by_duration(df)
    
    plt.subplot(2, 1, 1)
    plt.plot(
        range(len(sorted_df)), 
        sorted_df['audio_duration_seconds'].values, 
        marker='o', 
        linestyle='-', 
        linewidth=2, 
        markersize=4, 
        color='blue', 
        alpha=0.7
    )
    
    plt.xlabel('Номер аудиофайла (отсортированный по длительности)')
    plt.ylabel('Длительность (секунды)')
    plt.title('Распределение длительности аудиофайлов природы')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 1, 2)
    plt.hist(
        df['audio_duration_seconds'], 
        bins=12, 
        alpha=0.7, 
        color='green', 
        edgecolor='black', 
        linewidth=1.2
    )
    plt.xlabel('Длительность (секунды)')
    plt.ylabel('Количество файлов')
    plt.title('Гистограмма распределения длительности')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_plot, dpi=300, bbox_inches='tight')
    plt.show()


def demonstrate_dataframe_operations(df):
    """Демонстрирует различные операции с DataFrame."""
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ОПЕРАЦИЙ С DATAFRAME")
    print("=" * 60)
    
    print("\n1. Информация о DataFrame:")
    print(f"   Размер: {df.shape}")
    print(f"   Колонки: {list(df.columns)}")
    
    print("\n2. Типы данных:")
    print(df.dtypes)
    
    print("\n3. Статистика длительностей:")
    print(df['audio_duration_seconds'].describe())
    
    print("\n4. Топ-5 самых длинных аудиофайлов:")
    longest = df.nlargest(5, 'audio_duration_seconds')[
        ['audio_relative_path', 'audio_duration_seconds']
    ]
    for idx, row in longest.iterrows():
        filename = os.path.basename(row['audio_relative_path'])
        duration = row['audio_duration_seconds']
        print(f"   {filename}: {duration:.2f} сек")
    
    print("\n5. Топ-5 самых коротких аудиофайлов:")
    shortest = df.nsmallest(5, 'audio_duration_seconds')[
        ['audio_relative_path', 'audio_duration_seconds']
    ]
    for idx, row in shortest.iterrows():
        filename = os.path.basename(row['audio_relative_path'])
        duration = row['audio_duration_seconds']
        print(f"   {filename}: {duration:.2f} сек")


def main():
    """Основная функция для анализа длительности аудиофайлов."""
    parser = argparse.ArgumentParser(
        description='Анализ длительности аудиофайлов природы'
    )
    parser.add_argument(
        '--csv', 
        required=True, 
        help='Путь к CSV файлу с аннотацией'
    )
    parser.add_argument(
        '--output_csv', 
        default='audio_analysis.csv', 
        help='Путь для сохранения результата'
    )
    parser.add_argument(
        '--output_plot', 
        default='durations_plot.png', 
        help='Путь для сохранения графика'
    )
    parser.add_argument(
        '--min_duration', 
        type=float, 
        default=0, 
        help='Минимальная длительность для фильтрации'
    )
    parser.add_argument(
        '--max_duration', 
        type=float, 
        default=None, 
        help='Максимальная длительность для фильтрации'
    )
    parser.add_argument(
        '--demo', 
        action='store_true', 
        help='Показать демонстрацию операций с DataFrame'
    )
    
    args = parser.parse_args()
    
    print("Создание DataFrame из аннотации...")
    audio_df = create_audio_dataframe(args.csv)
    print(f"Загружено {len(audio_df)} аудиофайлов")
    
    print("Добавление колонки с длительностью...")
    audio_df = add_mock_duration_column(audio_df)
    
    original_count = len(audio_df)
    if args.min_duration > 0 or args.max_duration is not None:
        print("Применение фильтрации по длительности...")
        audio_df = filter_by_duration(
            audio_df, 
            args.min_duration, 
            args.max_duration
        )
        print(
            f"После фильтрации осталось {len(audio_df)} "
            f"файлов из {original_count}"
        )
    
    print("Сортировка по длительности...")
    audio_df = sort_by_duration(audio_df)
    
    print(f"Сохранение DataFrame в {args.output_csv}...")
    audio_df.to_csv(args.output_csv, index=False, encoding='utf-8')

    print(f"Создание графика в {args.output_plot}...")
    plot_durations(audio_df, args.output_plot)

    print("\n" + "=" * 50)
    print("СТАТИСТИКА ДЛИТЕЛЬНОСТЕЙ:")
    print("=" * 50)
    print(f"Общее количество файлов: {len(audio_df)}")
    print(f"Минимальная длительность: {audio_df['audio_duration_seconds'].min():.2f} сек")
    print(f"Максимальная длительность: {audio_df['audio_duration_seconds'].max():.2f} сек")
    print(f"Средняя длительность: {audio_df['audio_duration_seconds'].mean():.2f} сек")
    print(f"Медианная длительность: {audio_df['audio_duration_seconds'].median():.2f} сек")
    print(f"Стандартное отклонение: {audio_df['audio_duration_seconds'].std():.2f} сек")
    
    if args.demo:
        demonstrate_dataframe_operations(audio_df)


if __name__ == "__main__":
    main()