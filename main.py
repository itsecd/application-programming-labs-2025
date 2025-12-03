import soundfile as fs
import matplotlib.pyplot as plt
import argparse
import random
from typing import Optional
from pathlib import Path
import numpy as np
import pandas as pd


def get_two_audio_paths(csv_path: Path, rows_indexes: tuple[int, int]) -> Optional[tuple[Path, Path]]:
    """
    Получение относительных путей из .csv файла.
    """

    csv_path = Path(csv_path)

    if csv_path.exists():
        df = pd.read_csv(csv_path)
        first_ind, second_ind = rows_indexes

        if first_ind < len(df) and second_ind < len(df):
            audio_paths = df.iloc[rows_indexes, 0]
            print(f"audio_paths")
            return audio_paths
        else:
            print(f"These indexes are not valid")
            return None

    else:
        print(f"File with this path no exists")
        return None


def download_audio(audio_path: Path) -> tuple[np.ndarray, int]:
    """
    Скачивание файла.
    """

    data, samplerate = fs.read(audio_path)
    print(f"Sample array: {data}")
    print(f"Size (number of samples): {len(data)}")
    print(f"Sampling rate: {samplerate}")
    return data, samplerate


def save_audio(audio_path: Path, data: np.ndarray, samplerate: int) -> None:
    """
    Сохранение файла.
    """

    fs.write(audio_path, data, samplerate)
    print(f'Saved as {audio_path}')
    return None


def merge_two_audio(audio_path: Path, data1: np.ndarray, data2: np.ndarray, samplerate1: int) -> tuple[np.ndarray, int]:
    """
    Смешивание двух аудио файлов.
    """

    if len(data1) != len(data2):
            if len(data1) > len(data2):
                if data2.ndim == 1:
                    data2 = np.pad(data2, (0, len(data1) - len(data2)), 'constant')
                else:
                    padding = np.zeros((len(data1) - len(data2), data2.shape[1]))
                    data2 = np.vstack([data2, padding])

            else:
                if data1.ndim == 1:
                    data1 = np.pad(data1, (0, len(data2) - len(data1)), 'constant')
                else:
                    padding = np.zeros((len(data2) - len(data1), data1.shape[1]))
                    data1 = np.vstack([data1, padding])

    samplerate = samplerate1

    if data1.ndim == 1 and data2.ndim == 2:
        data1_stereo = np.column_stack([data1, data1])
        merge_data = data1_stereo + data2

    elif data1.ndim == 2 and data2.ndim == 1:
        data2_stereo = np.column_stack([data2, data2])
        merge_data = data1 + data2_stereo

    else:
        merge_data = data1 + data2

    save_audio(audio_path, merge_data, samplerate)
    return merge_data, samplerate


def demonstrate_result(data: np.ndarray, new_data: np.ndarray, samplerate: int) -> None:
    """
    Демонстрация графиков одного из изначальных файлов и получившегося файла.
    """

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Audio Comparison', fontsize=14, fontweight='bold')
    
    max_data = np.max(np.abs(data))
    max_new_data = np.max(np.abs(new_data))
    y_max = max(max_data, max_new_data) * 1.1

    ax1 = axes[0]
    duration_original = len(data) / samplerate
    x_original = np.linspace(0, duration_original, len(data))
    
    if data.ndim == 2:
        ax1.plot(x_original, data[:, 0], label='Left channel', color='blue')
        ax1.plot(x_original, data[:, 1], label='Right channel', color='red')
    else:
        ax1.plot(x_original, data, label='Mono audio', color='blue')
    
    ax1.set_title('Original Audio')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Amplitude')
    ax1.axhline(0, color='black', linewidth=0.5, ls='--')
    ax1.grid(color='gray', linestyle='--', linewidth=0.3)
    ax1.legend()
    ax1.set_ylim([-y_max, y_max])
    

    ax2 = axes[1]
    duration_new = len(new_data) / samplerate
    x_new = np.linspace(0, duration_new, len(new_data))
    
    if new_data.ndim == 2:
        ax2.plot(x_new, new_data[:, 0], label='Left channel', color='blue')
        ax2.plot(x_new, new_data[:, 1], label='Right channel', color='red')
    else:
        ax2.plot(x_new, new_data, label='Mono audio', color='green')
    
    ax2.set_title('Mixed Audio')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Amplitude')
    # ax2.axhline(0, color='black', linewidth=0.5, ls='--')
    ax2.grid(color='gray', linestyle='--', linewidth=0.3)
    ax2.legend()
    ax2.set_ylim([-y_max, y_max])
    
    plt.tight_layout()
    plt.show()
    return None


def main():
    parser = argparse.ArgumentParser(description = "Merge of 2 audio files")
    parser.add_argument('input_file', type = str, help = "path to the annotation file")
    parser.add_argument('output_file', type = str, help = "name of the new file")
    parser.add_argument('--first_audio', '-f', type = int, help = "index of the first audio from 0 to 13")
    parser.add_argument('--second_audio', '-s',  type = int, help = "index of the second audio from 0 to 13")
    args = parser.parse_args()

    if args.first_audio is None:
        args.first_audio = random.randint(0, 13)
    if args.second_audio is None:
        args.second_audio = random.randint(0, 13)

    audio_indexes = [args.first_audio, args.second_audio]
    audio_paths = get_two_audio_paths(args.input_file, audio_indexes)
    first_data, first_samplerate = download_audio(audio_paths.iloc[0])
    second_data, second_samplerate = download_audio(audio_paths.iloc[1])
    new_audio, samplerate = merge_two_audio(args.output_file, first_data, second_data, first_samplerate)
    demonstrate_result(second_data, new_audio, samplerate)


if __name__ == "__main__":
    main()
