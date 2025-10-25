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


def quadratic_interp(signal, factor):
    """
    quadratic interp
    берется исходный массив индексов и расширяется в factor раз
    для трех соседних точек вычисляется уравнение параболы,
    на сонове него между этими точками вставляются дополнительные сэмплы
    """
    if factor <= 0:
        raise ValueError("factor must be > 0")

    n_samples = int(len(signal) * factor)
    old_indices = np.arange(len(signal))
    new_indices = np.linspace(0, len(signal) - 1, n_samples)

    if signal.ndim == 1:
        new_signal = np.zeros(n_samples)
        channels = 1
    else:
        channels = signal.shape[1]
        new_signal = np.zeros((n_samples, channels))

    for i, x in enumerate(new_indices):
        x1 = int(np.floor(x))
        x0 = max(x1 - 1, 0)
        x2 = min(x1 + 1, len(signal) - 1)

        if channels == 1:
            y0, y1, y2 = signal[x0], signal[x1], signal[x2]
            t = x - x0
            a = y0 / 2 - y1 + y2 / 2
            b = -y0 + y1 - a
            c = y0
            new_signal[i] = a * t**2 + b * t + c
        else:
            for ch in range(channels):
                y0, y1, y2 = signal[x0, ch], signal[x1, ch], signal[x2, ch]
                t = x - x0
                a = y0 / 2 - y1 + y2 / 2
                b = -y0 + y1 - a
                c = y0
                new_signal[i, ch] = a * t**2 + b * t + c

    return new_signal


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
        # linear interp y = { (y1 - y0)/(x1 - x0) } * (x - x0) + y0
        new_signal = np.interp(new_indices, old_indices, signal)
    else:
        new_signal = np.zeros((n_samples, signal.shape[1]))
        for ch in range(signal.shape[1]):
            new_signal[:, ch] = np.interp(new_indices, old_indices, signal[:, ch])

    return new_signal


def plot_audio(original, modified, samplerate, factor, method, filename):
    time_orig = np.linspace(0, len(original)/samplerate, len(original))
    time_mod = np.linspace(0, len(modified)/samplerate, len(modified))

    plt.figure(figsize=(12,6))
    plt.subplot(2,1,1)
    plt.title("input audio")
    plt.plot(time_orig, original)
    plt.xlabel("time (с)")
    plt.ylabel("amplitude")

    plt.subplot(2,1,2)
    plt.title(f"{method} interpolation, factor={factor}")
    plt.plot(time_mod, modified, color='orange')
    plt.xlabel("time (с)")
    plt.ylabel("amplitude")

    plt.tight_layout()
    plt.savefig(filename)
    print(f"picture save: {filename}")
    plt.close()


def save_audio(file_path, data, samplerate):
    sf.write(file_path, data, samplerate)
    print(f"audio save: {file_path}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="path/to/input/track/file")
    parser.add_argument("-o", "--output", default="./result", help="path/to/output/track")
    parser.add_argument("--linear", action="store_true", default=True, help="use linear interp")
    parser.add_argument("--quadratic", action="store_true", help="use quadratic interp")
    parser.add_argument("--factor", type=float, default=2.0, help="speed factor (f.e. 2 = x2 slower)")
    return parser.parse_args()


def main():
    args = parse_args()

    data, sr = read_audio(args.input)

    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)

    if args.linear and not args.quadratic:
        linear_file = os.path.join(output_dir, f"{args.input}_linear.wav")
        lin = change_speed_linear(data, args.factor) 
        save_audio(linear_file, lin, sr)
        plot_audio(data, lin, sr, args.factor, "linear", os.path.join(output_dir, f"{args.input}_linear_plot.png"))

    if args.quadratic:
        quadratic_file = os.path.join(output_dir, f"{args.input}_quadratic.wav")
        quad = quadratic_interp(data, args.factor)
        save_audio(quadratic_file, quad, sr)
        plot_audio(data, quad, sr, args.factor, "quadratic", os.path.join(output_dir, f"{args.input}_quadratic_plot.png"))


if __name__ == "__main__":
    main()
