import argparse
from pathlib import Path
from typing import Optional

from dataframe_operations import (
    load_dataframe_from_csv,
    add_image_width_column,
    filter_by_width,
    sort_by_width,
    save_dataframe
)
from plotting import create_width_distribution_plot


def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.
    """
    parser = argparse.ArgumentParser(
        description='Анализ изображений: загрузка, обработка, сортировка и визуализация',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s --csv_input annotation.csv
  %(prog)s --csv_input annotation.csv --sort_order desc
  %(prog)s --csv_input annotation.csv --min_width 300 --max_width 1000
  %(prog)s --csv_input annotation.csv --csv_output results.csv --plot_output plot.png
        """
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
        help='Путь для сохранения обработанного DataFrame (по умолчанию: ./image_analysis.csv)'
    )
    parser.add_argument(
        '--plot_output',
        type=str,
        default='./width_distribution.png',
        help='Путь для сохранения графика (по умолчанию: ./width_distribution.png)'
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
        help='Минимальная ширина для фильтрации (необязательно)'
    )
    parser.add_argument(
        '--max_width',
        type=int,
        default=None,
        help='Максимальная ширина для фильтрации (необязательно)'
    )
    
    return parser.parse_args()


def validate_arguments(args: argparse.Namespace) -> Optional[str]:
    """
    Проверяет корректность аргументов.
    """
    if not Path(args.csv_input).exists():
        return f"Ошибка: файл {args.csv_input} не найден"
    
    if args.min_width is not None and args.min_width <= 0:
        return "Ошибка: минимальная ширина должна быть положительным числом"
    
    if args.max_width is not None and args.max_width <= 0:
        return "Ошибка: максимальная ширина должна быть положительным числом"
    
    if (args.min_width is not None and args.max_width is not None and 
        args.min_width > args.max_width):
        return "Ошибка: минимальная ширина не может быть больше максимальной"
    
    return None


def main() -> None:
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
        initial_count = len(df)
        df = add_image_width_column(df)
        removed_count = initial_count - len(df)
        
        if removed_count > 0:
            print(f"Удалено записей с ошибками: {removed_count}")
        print(f"Колонка добавлена. Валидных записей: {len(df)}")
        
        if df.empty:
            print("Ошибка: не удалось обработать ни одного изображения")
            return
        
        if args.min_width is not None or args.max_width is not None:
            print(f"\nФильтрация по ширине...")
            original_count = len(df)
            
            if args.min_width is not None:
                print(f"Минимальная ширина: {args.min_width} px")
            if args.max_width is not None:
                print(f"Максимальная ширина: {args.max_width} px")
            
            df = filter_by_width(df, args.min_width, args.max_width)
            
            filtered_count = len(df)
            print(f"Записей до фильтрации: {original_count}")
            print(f"Записей после фильтрации: {filtered_count}")
            print(f"Отфильтровано: {original_count - filtered_count}")
            
            if df.empty:
                print("Предупреждение: после фильтрации не осталось данных")
                return
        
        order = "возрастанию" if args.sort_order == 'asc' else "убыванию"
        print(f"\nСортировка по {order} ширины...")
        ascending = (args.sort_order == 'asc')
        df = sort_by_width(df, ascending=ascending)
        
        print("Первые 5 записей после сортировки:")
        print(df[['filename', 'image_width']].head())
        
        print(f"\nСоздание графика...")
        create_width_distribution_plot(df, args.plot_output)
        print(f"График сохранен в: {args.plot_output}")
        
        save_dataframe(df, args.csv_output)
        print(f"DataFrame сохранен в: {args.csv_output}")
        
        print("\n" + "="*60)
        print("ОБРАБОТКА ЗАВЕРШЕНА УСПЕШНО!")
        print("="*60)
        print(f"Обработано изображений: {len(df)}")
        print(f"DataFrame сохранен: {args.csv_output}")
        print(f"График сохранен: {args.plot_output}")
        
    except Exception as e:
        print(f"\nОшибка при выполнении программы: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()