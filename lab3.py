import argparse
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt


def download_audio (file_path) -> tuple:
    """
    загружает аудио и выводит данные о нём
    """
    data, samplerate = sf.read(file_path)
    quantity_samples = len(data)
    
    print(f"Массив сэмплов: {data}")
    print(f"Размер (количество сэмплов): {quantity_samples}")
    print(f"Частота дискретизации: {samplerate}")
    return data, samplerate


def less_amplitude (data, delta) -> "array":
    """
    уменьшает амплитуду сэмплов на заданную величину
    """

    if delta < 0 or delta > 1:
        raise ValueError("Уменьшать амплитуду можно на значение из диапазона от 0 до 1")

    less_data = data*(1-delta)
    new_data = np.clip(less_data, -1.0, 1.0)
    return new_data


def demonstration_result (data, new_data, samplerate, delta) -> None:
    """
    демонстрирует в виде графиков исходное аудио и изменённое аудио
    """
    duration = len(data)/samplerate
    x = np.linspace(0, duration, len(data))

    plt.figure(figsize=(10,5))

    if len(data.shape) > 1:
        y_left = data[:, 0]
        y_right = data[:, 1]

        plt.plot(x, y_left, label='Левый канал', color='blue')
        plt.plot(x, y_right, label='Правый канал', color='red')
    else:
        y = data

        plt.plot(x, y, label='Моно аудио', color='blue')

    plt.title('График исходного аудио')
    plt.xlabel('Время')
    plt.ylabel('Амплитуда')
    plt.axhline(0, color='black', linewidth=0.9, ls='--')
    plt.axvline(0, color='black', linewidth=0.9, ls='--')
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.3)
    plt.legend()


    plt.figure(figsize=(10,5))

    if len(new_data.shape) > 1:
        y_left = new_data[:, 0]
        y_right = new_data[:, 1]

        plt.plot(x, y_left, label='Левый канал', color='blue')
        plt.plot(x, y_right, label='Правый канал', color='red')
    else:
        y = new_data

        plt.plot(x, y, label='Моно аудио', color='blue')

    plt.title('График изменённого аудио')
    plt.xlabel('Время')
    plt.ylabel('Амплитуда')
    plt.axhline(0, color='black', linewidth=0.9, ls='--')
    plt.axvline(0, color='black', linewidth=0.9, ls='--')
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.3)
    plt.legend()

    plt.show()


def save_audio (data, output_path, samplerate) -> None:
    """
    сохраняет аудио
    """
    sf.write(output_path, data, samplerate)
    print(f"Сохранено в {output_path}")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Путь к аудиофайлу")
    parser.add_argument("-o", "--output", type=str, help="Путь для сохранения изменённого аудио файла")
    parser.add_argument("-d", "--delta", type=float, help="Величина уменьшения амплитуды (от 0 до 1)")
    args = parser.parse_args()

    try:
        data, samplerate = download_audio(args.input)
        new_data = less_amplitude(data, args.delta)
        save_audio(new_data, args.output, samplerate)
        demonstration_result(data, new_data, samplerate, args.delta)
        
    except Exception as error:
        print(f"Произошла ошибка: {error}")

if __name__ == "__main__":
    main()