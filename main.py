import argparse
from pathlib import Path
from typing import Optional

from core import (
    load_dataframe_from_csv,
    add_image_width_column,
    filter_by_width,
    sort_by_width,
    save_dataframe
)
from image_viewer import create_width_distribution_plot 


def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.
    """
    
    parser = argparse.ArgumentParser(
        description='Анализ изображений: загрузка, обработка, сортировка и визуализация'
    )

    parser.add_argument(
        '--csv_input',
        type=str,
        required=True,
        help='Путь к CSV файлу с аннотацией из лабораторной работы 2'
    )
    parser.add_argument(
        '--csv_output',
        type=str,
        default='./image_analysis.csv',
        help='Путь для сохранения обработанного DataFrame'
    )
    parser.add_argument(
        '--plot_output',
        type=str,
        default='./width_distribution.png',
        help='Путь для сохранения графика'
    )
    parser.add_argument(
        '--sort_order',
        type=str,
        choices=['asc', 'desc'],
        default='asc',
        help='Порядок сортировки: asc (по возрастанию) или desc (по убыванию)'
    )
    parser.add_argument(
        '--min_width',
        type=int,
        default=None,
        help='Минимальная ширина для фильтрации'
    )
    parser.add_argument(
        '--max_width',
        type=int,
        default=None,
        help='Максимальная ширина для фильтрации'
    )

    return parser.parse_args()


def validate_arguments(args: argparse.Namespace) -> Optional[str]:
    """
    Проверяет валидность аргументов командной строки.
    """
    
    if not Path(args.csv_input).exists():
        return f"Ошибка: файл {args.csv_input} не найден"

    return None


def main() -> None:
    """
    Основная функция программы.
    """

    args = parse_arguments()

    error_message = validate_arguments(args)
    if error_message:
        print(error_message)
        return

    try:
        print(f"Загрузка данных из: {args.csv_input}")
        df = load_dataframe_from_csv(args.csv_input)
        print(f"Загружено записей: {len(df)}")

        print("\nДобавление колонки с шириной изображений...")
        df = add_image_width_column(df)
        print(f"Валидных записей: {len(df)}")

        if args.min_width is not None or args.max_width is not None:
            df = filter_by_width(df, args.min_width, args.max_width)
            print(f"После фильтрации: {len(df)} записей")

        ascending = (args.sort_order == 'asc')
        df = sort_by_width(df, ascending=ascending)

        print("Создание графика...")
        create_width_distribution_plot(df, args.plot_output)

        save_dataframe(df, args.csv_output)

        print(f"Обработано изображений: {len(df)}")
        print(f"DataFrame сохранен: {args.csv_output}")
        print(f"График сохранен: {args.plot_output}")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()