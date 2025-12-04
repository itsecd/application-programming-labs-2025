import matplotlib.pyplot as plt
import numpy
import soundfile


def get_audio(filepath: str) -> tuple[list[numpy.ndarray], int]:
    """
    Возвращает массив сэмплов и частоту дискретизации
    """
    try:
        data = soundfile.read(filepath)
        sample_array = data[0]
        samplerate = data[-1]
        return sample_array, samplerate
    except FileNotFoundError as e:
        raise e(f"Файл по такому пути ({filepath}) не найден, увынск(")


def reverse_audio(data: list[numpy.ndarray]) -> list[numpy.ndarray]:
    """
    Переворачивает аудио задом наперёд
    """
    return data[::-1]


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