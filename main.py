import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np


def show_plots(data, noise, noise_data) -> None:
    """
    Задача данной функции - создать несколько графиков для полученных результатов
    """
    REDUCE_CONST = 100 # Чтобы не перегружать matplotlib

    fig, ax = plt.subplots(nrows=3)
    data_plt = ax[0]
    noise_plt = ax[1]
    noise_data_plt = ax[2]

    data_plt.plot(data[:len(data)//REDUCE_CONST*REDUCE_CONST].reshape(-1, REDUCE_CONST).mean(axis=1)) 
    data_plt.set_xticklabels([])
    data_plt.set_title("Исходный звук")
    data_plt.set_ylim(-1, 1)

    noise_plt.plot(noise[:len(noise)//REDUCE_CONST*REDUCE_CONST].reshape(-1, REDUCE_CONST).mean(axis=1))
    noise_plt.set_xticklabels([])
    noise_plt.set_title("Белый шум")
    noise_plt.set_ylim(-1, 1)

    noise_data_plt.plot(noise_data[:len(noise_data)//REDUCE_CONST*REDUCE_CONST].reshape(-1, REDUCE_CONST).mean(axis=1))
    noise_data_plt.set_xticklabels([])
    noise_data_plt.set_title("Результат")
    noise_data_plt.set_ylim(-1, 1)
    plt.show()


def main(file_path: str, output_path: str) -> None:
    """ 
    Основная логика программы 
    Args:
        file_path (str): Путь до обрабатываемого файла
        output_path (str): Путь для сохранения результата
    """

    data, samplerate = sf.read(file_path)
    print(f"Частота дискретизации: {samplerate} Гц.")
    noise = np.random.normal(loc=0, scale=0.02, size=(data.shape)) # Массив случайных значений шума.
    noise_data = data + noise
    sf.write(output_path, noise_data, samplerate)

    show_plots(data, noise, noise_data)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="Аудиофайл для обработки")
    parser.add_argument("-o", "--out", type=str, help="Путь для сохранения результата", default="out.mp3")
    args = parser.parse_args()

    try:
        main(args.file, args.out)
    except FileNotFoundError as e:
        print(f'Ошибка, не найден файл: "{e.filename}"')
    except PermissionError as e:
        print(f"Недостаточно прав для совершения операции: {e}")