import argparse
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt


def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.
    """
    parser = argparse.ArgumentParser(description="Реверс аудиофайла и визуализация сигнала")
    parser.add_argument('file', type=str, help='Путь к исходному аудиофайлу')
    parser.add_argument('new_file', type=str, help='Путь для сохранения реверснутого файла')
    return parser.parse_args()


def load_audio(filepath: str) -> tuple[np.ndarray, int]:
    """
    Загружает аудиофайл и возвращает данные и частоту дискретизации.
    """
    try:
        data, samplerate = sf.read(filepath)
        return data, samplerate
    except Exception as e:
        raise RuntimeError(f"Не удалось загрузить аудиофайл '{filepath}': {e}")


def reverse_audio(data: np.ndarray) -> np.ndarray:
    """
    Реверсирует аудиоданные по временной оси.
    """
    return data[::-1]


def save_audio(filepath: str, data: np.ndarray, samplerate: int) -> None:
    """
    Сохраняет аудиоданные в файл.
    """
    sf.write(filepath, data, samplerate)


def prepare_time_axis(data: np.ndarray, samplerate: int) -> np.ndarray:
    """
    Создаёт временную ось для визуализации.
    """
    duration = len(data) / samplerate
    return np.linspace(0, duration, len(data))


def extract_channel_for_plot(data: np.ndarray) -> np.ndarray:
    """
    Извлекает канал для визуализации (левый — если стерео, иначе моно).
    """
    if data.ndim == 2:
        return data[:, 0]
    return data


def plot_signals(orig_signal: np.ndarray, rev_signal: np.ndarray, time_axis: np.ndarray) -> None:
    """
    Строит графики исходного и реверснутого сигналов.
    """
    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    plt.plot(time_axis, orig_signal, color='blue')
    plt.title("Исходный сигнал")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(time_axis, rev_signal, color='red')
    plt.title("Реверснутый сигнал")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def main() -> None:
    """
    Основная функция программы.
    """
    args = parse_arguments()

    # Загрузка
    data, samplerate = load_audio(args.file)
    print(f"Исходный массив: форма = {data.shape}, частота дискретизации = {samplerate} Гц")

    # Реверс
    reversed_data = reverse_audio(data)
    print(f"Реверснутый массив: форма = {reversed_data.shape}")

    # Сохранение
    save_audio(args.new_file, reversed_data, samplerate)

    # Подготовка данных для графика
    time_axis = prepare_time_axis(data, samplerate)
    orig_to_plot = extract_channel_for_plot(data)
    rev_to_plot = extract_channel_for_plot(reversed_data)

    # Визуализация
    plot_signals(orig_to_plot, rev_to_plot, time_axis)


if __name__ == '__main__':
    main()
