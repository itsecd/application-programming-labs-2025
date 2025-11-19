import argparse
from data_processing import create_df, add_amplitude, sort_by_amplitude, filtr_amplitude
from visualization import plot_amplitude_histogram


def parse_arguments() -> argparse.Namespace:
    """Парсит аргументы командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_csv", help="Путь к csv")
    parser.add_argument("--min", type=float, help="минимальное значение фильтрации")
    parser.add_argument("--max", type=float, help="максимальное значение фильтрации")
    return parser.parse_args()


def main():
    try:
        args = parse_arguments()
        df = create_df(args.input_csv)
        df = add_amplitude(df)
        plot_amplitude_histogram(df)
    except Exception as e:
        print(f"Ошибка при выполнении программы: {e}")

if __name__ == '__main__':
    main()
