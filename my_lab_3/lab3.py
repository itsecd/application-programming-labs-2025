import argparse
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки
    """
    parser = argparse.ArgumentParser(description="Парсинг звуков с mixkit.co")
    parser.add_argument('file', type=str, help='исходный файл')
    parser.add_argument('new_file', type=str, help='путь сохранения файла')
    return parser.parse_args()

def main():
    """
    """
    args=parse_arguments()
    sound_file = args.file
    new_file = args.new_file
    data, samplerate = sf.read(sound_file)
    print(f"Массив сэмплов: {data}")
    print(f"Частота дискретизации: {samplerate}")
    print(f"Исходный массив: форма = {data.shape}, частота дискретизации = {samplerate} Гц")
    new_data = data[::-1]
    print(f"Реверснутый массив: форма = {new_data.shape}")
    sf.write(new_file, new_data, samplerate)
    #Визуализация
    duration = len(data) / samplerate
    time_axis = np.linspace(0, duration, len(data))
    if data.ndim == 2:
        orig_signal = data[:, 0]
        rev_signal = new_data[:, 0]
        print("Файл стерео: отображается левый канал.")
    else:
        orig_signal = data
        rev_signal = new_data

    plt.figure(figsize=(14, 6))
    #Исходный
    plt.subplot(1, 2, 1)
    plt.plot(time_axis, orig_signal, color='blue')
    plt.title("Исходный сигнал")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")
    plt.grid(True)
    #Реверснутый
    plt.subplot(1, 2, 2)
    plt.plot(time_axis, rev_signal, color='red')
    plt.title("Реверснутый сигнал")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    
if __name__ == '__main__':
    main()
