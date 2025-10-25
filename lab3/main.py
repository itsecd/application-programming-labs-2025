import os
import argparse 
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

def read_audio(file_path):
    data, samplerate = sf.read(file_path)
    print(f"audio size(samples): {len(data)}")
    print(f"Time: {len(data) / samplerate:.2f} sec")
    return data, samplerate


def change_speed_linear(signal, factor):
    """
    linear interp
    берется исходный массив сэмплов (значений амплитуд), 
    создается новый массив в factor раз больше и равномерно 
    вычисялется уравнение прямой между двумя старыми точками
    и на основе него между ними вставляются еще сколько-то сэмплов
    """
    if factor == 1.0:
        return signal

    n_samples = int(len(signal) * factor)
    old_indices = np.arange(len(signal))
    new_indices = np.linspace(0, len(signal) - 1, n_samples)

    if signal.ndim == 1:
        new_signal = np.interp(new_indices, old_indices, signal)
    else:
        new_signal = np.zeros((n_samples, signal.shape[1]))
        for ch in range(signal.shape[1]):
            new_signal[:, ch] = np.interp(new_indices, old_indices, signal[:, ch])

    return new_signal


def plot_audio(original, modified, samplerate, factor, method, file_path):
    time_orig = np.linspace(0, len(original)/samplerate, len(original))
    time_mod = np.linspace(0, len(modified)/samplerate, len(modified))

    plt.figure(figsize=(13,7))
    plt.subplot(2,1,1)
    plt.title("input audio")
    plt.plot(time_orig, original)
    plt.xlabel("time (с)")
    plt.ylabel("Amplitude")

    plt.subplot(2,1,2)
    plt.title(f"{method} interpolation, factor={factor}")
    plt.plot(time_mod, modified, color='orange')
    plt.xlabel("time (с)")
    plt.ylabel("Amplitude")

    plt.tight_layout()
    plt.savefig(file_path)
    print(f"picture save: {file_path}")
    plt.close()


def save_audio(file_path, data, samplerate):
    sf.write(file_path, data, samplerate)
    print(f"audio save: {file_path}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="path/to/input/track/file")
    parser.add_argument("-o", "--output", default="./result", help="path/to/output/track")
    parser.add_argument("--factor", type=float, default=2.0, help="speed factor (f.e. 2 = x2 slower)")
    return parser.parse_args()


def main():
    args = parse_args() 

    data, sr = read_audio(args.input)

    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, f"{args.input}_linear.mp3")
    mod_track = change_speed_linear(data, args.factor)
    save_audio(file_path, mod_track, sr)
    plot_audio(data, mod_track, sr, args.factor, "linear", os.path.join(output_dir, f"{args.input}_linear_plot.png"))


if __name__ == "__main__":
    main()

