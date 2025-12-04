import argparse
from func import (
    get_audio,
    reverse_audio,
    plot_audio,
)
import soundfile


def parser_func() -> tuple[str, str] :
    """
    Функция для ввода путей файлов ввода и вывода
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='Path to input file')
    parser.add_argument('output_file', type=str, help='Path to output file')

    args = parser.parse_args()
    return args.input_file, args.output_file


def main():
    """
    Главная функция, которая управляет работой программы
    """
    try:
        input_file, output_file = parser_func()
        input_data, input_samplerate = get_audio(input_file)
        print(f"Размер файла (кол-во сэмплов): {len(input_data)}")
        reverse_data = reverse_audio(input_data)
        soundfile.write(output_file, reverse_data, input_samplerate)
        plot_audio(input_data, reverse_data, input_samplerate)
    except Exception as e:
        print(f"В процессе работы программы произошла ошибка: {e}")


if __name__ == '__main__':
    main()
