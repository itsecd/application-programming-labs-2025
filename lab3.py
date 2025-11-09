import argparse
import numpy as np
import soundfile as sf


def add_white_noise(audio_data, noise_level=0.1):
    noise = np.random.normal(0, noise_level, audio_data.shape)
    noisy_audio = audio_data + noise
    return np.clip(noisy_audio, -1.0, 1.0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True, help='Аудиофайл для обработки')
    parser.add_argument('-o', '--out', help='Файл для сохранения результата', default="audio_with_white_noise.mp3")
    
    args = parser.parse_args()
    
    audio_data, sample_rate = sf.read(args.file)
    
    print(f"Размер аудио: {audio_data.shape}")
    print(f"Частота дискретизации: {sample_rate} Гц")
    
    noisy_audio = add_white_noise(audio_data, 0.1)
    
    sf.write(args.out, noisy_audio, sample_rate)
    print(f"Результат сохранен: {args.out}")


if __name__ == "__main__":
    main()
