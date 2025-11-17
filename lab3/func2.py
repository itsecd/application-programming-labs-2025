import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf


def get_args() -> argparse.Namespace:
    """Разбор аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Эхо-эффект для аудиофайла"
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Путь к исходному аудио (downloads/country/file.mp3)"
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Путь для сохранённого результата (echoaudios/funk/file_echo.mp3)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Задержка эхо (в секундах)"
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=1,
        help="Громкость отражённого сигнала"
    )
    return parser.parse_args()


def echo_effect(audio: np.ndarray, sr: int, delay: float, alpha: float) -> np.ndarray:
    """Применяет эффект эха к аудиосигналу.
    
    Args:
        audio (np.ndarray): Входной аудиосигнал (моно).
        sr (int): Частота дискретизации.
        delay (float): Задержка эхо в секундах.
        alpha (float): Коэффициент усиления отражённого сигнала.

    Returns:
        np.ndarray: Аудио с эхо-эффектом.
    """
    delay_samples = int(sr * delay)
    output = np.zeros(len(audio) + delay_samples, dtype=np.float32)
    output[:len(audio)] += audio.astype(np.float32)
    output[delay_samples:delay_samples + len(audio)] += alpha * audio.astype(np.float32)

    max_val = np.max(np.abs(output))
    if max_val > 1:
        output /= max_val

    return output


def plot_audio(original: np.ndarray, processed: np.ndarray, sr: int) -> None:
    """Отображает графики исходного и обработанного аудио.

    Args:
        original (np.ndarray): Исходный сигнал.
        processed (np.ndarray): Сигнал после эхо.
        sr (int): Частота дискретизации.
    """
    t_orig = np.linspace(0, len(original) / sr, len(original))
    t_proc = np.linspace(0, len(processed) / sr, len(processed))

    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(t_orig, original)
    plt.title("Исходное аудио")

    plt.subplot(2, 1, 2)
    plt.plot(t_proc, processed)
    plt.title("После эхо-эффекта")

    plt.tight_layout()
    plt.show()


def save_audio(filepath: str, audio: np.ndarray, sr: int) -> None:
    """Сохраняет аудио в файл, создавая недостающие папки.

    Args:
        filepath (str): Путь к файлу для сохранения.
        audio (np.ndarray): Аудио для сохранения.
        sr (int): Частота дискретизации.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    sf.write(filepath, audio, sr)
    print(f"Файл сохранён в: {filepath}")
