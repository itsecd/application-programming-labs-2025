import argparse
from analysis import (
    get_args,
    build_dataframe, 
    sort_dataframe,
    filter_dataframe,
    save_dataframe,
    plot_amplitudes
)


def main() -> None:
    """Основная функция программы"""
    args = get_args()
    
    print("Построение DataFrame...")
    df = build_dataframe(args.annotation)
    
    print("Сортировка по средней амплитуде...")
    sorted_df = sort_dataframe(df, 'средняя_амплитуда', ascending=True)
    
    print("Фильтрация амплитуд > 0.05...")
    filtered_df = filter_dataframe(sorted_df, 'средняя_амплитуда', min_value=0.05)
    
    print("Сохранение результатов...")
    save_dataframe(sorted_df, args.output_df)
    
    print("Построение графика...")
    plot_amplitudes(sorted_df, args.output_plot)
    
    print(f"Всего файлов: {len(df)}")
    print(f"После фильтрации: {len(filtered_df)}")
    print(f"Минимальная амплитуда: {df['средняя_амплитуда'].min():.4f}")
    print(f"Максимальная амплитуда: {df['средняя_амплитуда'].max():.4f}")
    print(f"Средняя амплитуда: {df['средняя_амплитуда'].mean():.4f}")


if __name__ == "__main__":
    try:
        args = get_args()
        main()
    except FileNotFoundError as e:
        print(f'Ошибка: Файл не найден - "{e}"')
    except Exception as e:
        print(f'Непредвиденная ошибка: {e}')