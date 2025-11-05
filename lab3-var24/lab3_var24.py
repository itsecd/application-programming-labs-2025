import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf


def load_audio(filepath: str) -> np.ndarray:
    """Загружает аудиофайл"""
    try:
        data, _ = sf.read(filepath)
        return data
    except FileNotFoundError:
        raise


def create_echo(audio_data: np.ndarray, delay_samples: int, decay: float) -> np.ndarray:
    """Создаёт эхо-эффект путём наложения задержанного сигнала"""
    output_size = len(audio_data) + delay_samples

    if len(audio_data.shape) == 1:
        result = np.zeros(output_size, dtype=audio_data.dtype)
    else:
        result = np.zeros(
            (output_size, audio_data.shape[1]), dtype=audio_data.dtype
        )

    result[: len(audio_data)] = audio_data
    result[delay_samples : delay_samples + len(audio_data)] += (
        audio_data * decay
    )

    return result


def save_audio(audio_data: np.ndarray, filepath: str, samplerate: int) -> None:
    """Сохраняет аудиофайл"""
    sf.write(filepath, audio_data, samplerate)


def visualize(original: np.ndarray,echo: np.ndarray,delay_samples: int,samplerate: int,) -> None:
    """Визуализирует исходный и обработанный сигналы"""

    samples_to_show = min(samplerate * 2, len(original))
    time_axis = np.arange(samples_to_show) / samplerate

    plt.figure(figsize=(14, 8))

    plt.subplot(2, 1, 1)
    plt.plot(
        time_axis,
        original[:samples_to_show],
        color="blue",
        linewidth=0.5,
    )
    plt.title("Исходный сигнал", fontsize=12, fontweight="bold")
    plt.xlabel("Время (сек)")
    plt.ylabel("Амплитуда")
    plt.grid(True, alpha=0.3)
    plt.ylim(-1.1, 1.1)

    plt.subplot(2, 1, 2)
    echo_to_show = min(samples_to_show, len(echo))
    plt.plot(
        time_axis[:echo_to_show],
        echo[:echo_to_show],
        color="green",
        linewidth=0.5,
    )
    plt.title("Сигнал с эхо-эффектом", fontsize=12, fontweight="bold")
    plt.xlabel("Время (сек)")
    plt.ylabel("Амплитуда")
    plt.grid(True, alpha=0.3)
    plt.ylim(-1.1, 1.1)

    delay_seconds = delay_samples / samplerate
    plt.figtext(
        0.5,
        0.02,
        f"Задержка: {delay_seconds:.3f} сек ({delay_samples} сэмплов)",
        ha="center",
        fontsize=10,
    )

    plt.tight_layout()
    plt.show()


def parse_arguments() -> argparse.Namespace:
    """Парсит аргументы командной строки"""

    parser = argparse.ArgumentParser(description="Применяет эхо-эффект к аудиофайлу")
    parser.add_argument("--input",required=True,help="Путь к исходному аудиофайлу",)
    parser.add_argument("--output",required=True,help="Путь для сохранения результата",)
    parser.add_argument("--delay",type=float,default=0.3,help="Задержка эхо в секундах ",)
    parser.add_argument("--decay",type=float,default=0.6,help="Коэффициент затухания ",)
    parser.add_argument("--samplerate",type=int,default=44100,help="Частота дискретизации для сохранения ",)
    return parser.parse_args()


def main() -> int:
    """Главная функция программы"""

    args = parse_arguments()

    try:
        
        audio_data = load_audio(args.input)

        delay_samples = int(args.delay * args.samplerate)
        echo_data = create_echo(audio_data, delay_samples, args.decay)

        visualize(audio_data, echo_data, delay_samples, args.samplerate)

        save_audio(echo_data, args.output, args.samplerate)

        return 0
    except Exception as e:
        print(f"Ошибка при выполнении программы: {e}")


if __name__ == "__main__":
    exit(main())