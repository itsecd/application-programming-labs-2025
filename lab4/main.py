import argparse
import os

from file_utils import (
    get_audio_path,
    add_min_ampl_col,
    sort_by,
    filter_by,
    save_dataframe
)
from visualization import plot_amplitude


def parse_args():
    """
    Парсит аргументы командной строки.
    """

    parser = argparse.ArgumentParser(
        description="Анализ аудиофалов"
    )
    parser.add_argument("--input", required=True,
                        help="Путь к исходным файлам")
    parser.add_argument("--output_df", default="output/df.csv",
                        help="Путь для сохранения DataFrame")
    parser.add_argument("--output_img", default="output/plt.jpg",
                        help="Путь для сохранения графика")
    parser.add_argument("--treshold", type=float, default=None,
                        help="Пороговое значение минимальной амплитуды")
    return parser.parse_args()


def main():
    try:
        args = parse_args()
        if not os.path.isdir(args.input):
            raise FileNotFoundError(f"Неверно указан путь: {args.input}")

        print("Анализ файлов...")
        df = get_audio_path(args.input)

        if df.empty:
            raise ValueError("Папка пуста")

        print("Вычисление минимальной амплитуды")
        df = add_min_ampl_col(df)

        print("Сортировка по амплитуде")
        df = sort_by(df)

        if args.treshold is not None:
            print(f"Фильтация по min_amplitude >= {args.treshold}")
            df = filter_by(df, args.treshold)
            if df.empty:
                raise ValueError("После фильтрации данных нет")

        print("Сохранение DataFrame")
        save_dataframe(df, args.output_df)

        print("Построение графика")
        plot_amplitude(df, args.output_img)
        print("Успешно.")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
