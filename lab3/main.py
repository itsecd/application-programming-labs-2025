import argparse
from audio_processing import read_audio_file, stereo_to_mono, limit_amplitude, save_audio
from plot_utils import plot_comparison

def main():
    parser = argparse.ArgumentParser(description="Ограничение амплитуды аудио")
    parser.add_argument('-f', '--file', required=True, help="Путь к исходному аудио (mp3/wav)")
    parser.add_argument('-o', '--out', default="audio_limited.mp3", help="Файл для сохранения результата")
    parser.add_argument('-t', '--threshold', type=float, required=True, help="Порог амплитуды (0.0–1.0)")

    args = parser.parse_args()

    audio, sr = read_audio_file(args.file)
    print(f"Размер аудио: {audio.shape}, частота дискретизации: {sr} Гц")

    mono_audio = stereo_to_mono(audio)
    limited_audio = limit_amplitude(mono_audio, args.threshold)

    save_audio(args.out, limited_audio, sr)
    print(f"Результат сохранен: {args.out}")

    plot_comparison(mono_audio, limited_audio, sr)

if __name__ == "__main__":
    main()
