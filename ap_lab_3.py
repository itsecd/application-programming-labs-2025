import argparse
import matplotlib.pyplot as plt
import numpy
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


def get_audio_info(filepath: str) -> tuple[list[numpy.ndarray], int]:
    """
    Возвращает массив сэмплов и частоту дискретизации
    """
    data = soundfile.read(filepath)[0]
    samplerate = soundfile.read(filepath)[-1]
    return data, samplerate


def reverse_audio(filepath: str) -> list[numpy.ndarray]:
    """
    Переворачивает аудио задом наперёд
    """
    try:
        data = soundfile.read(filepath)[0]
        return data[::-1]
    except FileNotFoundError as Open_File_Error:
        raise FileNotFoundError(f"Файл по такому пути ({filepath}) не найден, увынск(")


def plot_audio(original: numpy.ndarray, reversed_audio: numpy.ndarray, samplerate: int) -> None:
    """
    Рисует два графика рядом: оригинал и перевёрнутый
    """
    time_orig = numpy.arange(len(original)) / samplerate
    time_rev = numpy.arange(len(reversed_audio)) / samplerate

    plt.figure(figsize=(14, 6))

    plt.subplot(2, 1, 1)
    plt.plot(time_orig, original, color='blue', linewidth=0.8)
    plt.title("Исходный аудиофайл")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")
    plt.grid(True, alpha=0.3)

    plt.subplot(2, 1, 2)
    plt.plot(time_rev, reversed_audio, color='red', linewidth=0.8)
    plt.title("Результат")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def main():
    """
    Главная функция, которая управляет работой программы
    """
    try:
        input_file, output_file = parser_func()
        input_data, input_samplerate = get_audio_info(input_file)
        print(f"Размер файла (кол-во сэмплов): {len(input_data)}")
        reverse_data = reverse_audio(input_file)
        soundfile.write(output_file, reverse_data, input_samplerate)
        plot_audio(input_data, reverse_data, input_samplerate)
    except Exception as Open_File_Error:
        print(f"В процессе работы программы произошла ошибка: {Open_File_Error}")


if __name__ == '__main__':
    main()