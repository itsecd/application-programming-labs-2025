import argparse
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf


def add_white_noise(audio_data, noise_level=0.1):
    noise = np.random.normal(0, noise_level, audio_data.shape)
    noisy_audio = audio_data + noise
    return np.clip(noisy_audio, -1.0, 1.0)


def plot_comparison(original, noisy, sample_rate):
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True, help='Аудиофайл для обработки')
    parser.add_argument('-o', '--out', help='Файл для сохранения результата', default="audio_with_white_noise.mp3")
    
    args = parser.parse_args()
    
    # Читаем аудио
    audio_data, sample_rate = sf.read(args.file)
    
    print(f"Размер аудио: {audio_data.shape}")
    print(f"Частота дискретизации: {sample_rate} Гц")
    
    # Добавляем шум
    noisy_audio = add_white_noise(audio_data, 0.1)
    
    # Сохраняем результат
    sf.write(args.out, noisy_audio, sample_rate)
    print(f"Результат сохранен: {args.out}")
    
    # Показываем графики
    plot_comparison(audio_data, noisy_audio, sample_rate)


if __name__ == "__main__":
    main()
