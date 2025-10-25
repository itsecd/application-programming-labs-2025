import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
from audio_processor import AudioProcessor

def plot_audio(
    original: np.ndarray,
    modified: np.ndarray,
    samplerate: int,
    factor: float,
    method: str,
    filename: str
) -> None:
    time_orig: np.ndarray = np.linspace(0, len(original)/samplerate, len(original))
    time_mod: np.ndarray = np.linspace(0, len(modified)/samplerate, len(modified))

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="path/to/input/track/file")
    parser.add_argument("-o", "--output", default="./result", help="path/to/output/track")
    parser.add_argument("--linear", action="store_true", default=True, help="use linear interp")
    parser.add_argument("--quadratic", action="store_true", help="use quadratic interp")
    parser.add_argument("--factor", type=float, default=2.0, help="speed factor (f.e. 2 = x2 slower)")
    return parser.parse_args()


def process_and_plot(
    processor: AudioProcessor,
    interp_func: callable,
    factor: float,
    method: str,
    output_dir: str,
    base_name: str
) -> None:
    output_wav: str = os.path.join(output_dir, f"{base_name}_{method}.wav")
    output_plot: str = os.path.join(output_dir, f"{base_name}_{method}_plot.png")

    modified: np.ndarray = interp_func(factor)
    processor.save_audio(output_wav, modified)

    plot_audio(
        original=processor.data,
        modified=modified,
        samplerate=processor.samplerate,
        factor=factor,
        method=method,
        filename=output_plot
    )


def main() -> None:
    args = parse_args()

    if not os.path.isfile(args.input):
        print(f"error: file '{args.input}' not found!")
        return

    processor: AudioProcessor = AudioProcessor(args.input)
    processor.read_audio()

    output_dir: str = args.output
    os.makedirs(output_dir, exist_ok=True)

    if args.linear and not args.quadratic:
        process_and_plot(processor, processor.change_speed_linear, args.factor, "linear", output_dir, args.input)

    if args.quadratic:
        process_and_plot(processor, processor.quadratic_interp, args.factor, "quadratic", output_dir, args.input)


if __name__ == "__main__":
    main()

