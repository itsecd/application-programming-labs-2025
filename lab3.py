import argparse
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf


def add_white_noise(audio_data: np.ndarray, noise_level: float = 0.1) -> np.ndarray:
    """
    Добавляет белый шум к аудиоданным.
    
    Args:
        audio_data: Исходные аудиоданные
        noise_level: Уровень шума (от 0.0 до 1.0)
    
    Returns:
        Аудиоданные с добавленным белым шумом
    """
    noise = np.random.normal(0, noise_level, audio_data.shape)
    noisy_audio = audio_data + noise
    return np.clip(noisy_audio, -1.0, 1.0)


def plot_comparison(original: np.ndarray, noisy: np.ndarray, sample_rate: int) -> None:
    """
    Строит графики сравнения оригинального аудио и аудио с шумом.
    
    Args:
        original: Оригинальные аудиоданные
        noisy: Аудиоданные с шумом
        sample_rate: Частота дискретизации
    """
    samples_to_show = min(len(original), 2 * sample_rate)
    time = np.linspace(0, 2, samples_to_show)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
    
    ax1.plot(time, original[:samples_to_show], 'b-', linewidth=0.8)
    ax1.set_title('Исходное аудио')
    ax1.set_ylabel('Амплитуда')
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(time, noisy[:samples_to_show], 'r-', linewidth=0.8)
    ax2.set_title('Аудио с белым шумом')
    ax2.set_xlabel('Время (секунды)')
    ax2.set_ylabel('Амплитуда')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def read_audio_file(file_path: str) -> Tuple[np.ndarray, int]:
    """
    Читает аудиофайл и возвращает данные и частоту дискретизации.
    
    Args:
        file_path: Путь к аудиофайлу
    
    Returns:
        Кортеж (аудиоданные, частота дискретизации)
    """
    try:
        audio_data, sample_rate = sf.read(file_path)
        return audio_data, sample_rate
    except Exception as e:
        raise ValueError(f"Ошибка чтения файла {file_path}: {e}")


def main() -> None:
    """
    Основная функция программы.
    Обрабатывает аргументы командной строки и выполняет добавление шума к аудио.
    """
    parser = argparse.ArgumentParser(
        description='Добавление белого шума к аудиофайлу'
    )
    parser.add_argument('-f', '--file', required=True, help='Аудиофайл для обработки')
    parser.add_argument('-o', '--out', help='Файл для сохранения результата', default="audio_with_white_noise.mp3")
    
    args = parser.parse_args()
    
    try:
        audio_data, sample_rate = read_audio_file(args.file)
        
        print(f"Размер аудио: {audio_data.shape}")
        print(f"Частота дискретизации: {sample_rate} Гц")
        
        noisy_audio = add_white_noise(audio_data, 0.1)
        
        sf.write(args.out, noisy_audio, sample_rate)
        print(f"Результат сохранен: {args.out}")
        
        plot_comparison(audio_data, noisy_audio, sample_rate)
        
    except FileNotFoundError:
        print(f"Ошибка: файл '{args.file}' не найден")
    except ValueError as e:
        print(f"Ошибка обработки аудио: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
