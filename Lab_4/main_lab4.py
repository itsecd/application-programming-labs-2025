import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

from pathlib import Path
from iterator import FilePathIterator


def min_amplitude(file_path: Path) -> float:
    """
    Возвращает минимальную амплитуду (по модулю) аудиофайла.
    Если файл невозможно прочитать — возвращает 0.
    """
    if not file_path.exists():
        print(f"[WARNING] File does not exist: {file_path}")
        return 0.0
    
    data, samplerate = sf.read(file_path)
    abs_data = np.abs(data)
    return float(abs_data.min())

def set_dataframe (src: Path) -> pd.DataFrame:    
    """
    Создаёт DataFrame из CSV-файла (abs_path, rel_path)
    и вычисляет минимальную амплитуду для каждого файла.
    """
    absolute_paths = []
    relative_paths = []
    amplitudes = []

    it = FilePathIterator(src)
    for p in it:
        abs_path = p['abs_path']
        rel_path = p.get('rel_path', '')

        absolute_paths.append(abs_path)
        relative_paths.append(rel_path)
        amplitudes.append(min_amplitude(Path(abs_path)))
    
    df = pd.DataFrame({"abs_path": absolute_paths, "rel_path": relative_paths, "amplitudes": amplitudes})

    return df

def sort_amplitudes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Сортирует DataFrame по столбцу amplitudes.
    """
    sorted_df = df.sort_values(by='amplitudes')

    return sorted_df

def plot_sorted_min_amplitude(df: pd.DataFrame)->None:
    """
    Строит график минимальных амплитуд после сортировки.
    """   
    plt.figure(figsize=(12,6))
    plt.plot(range(len(df)), df['amplitudes'], marker='o', linewidth=1, markersize=3, color='blue')
    plt.title('Amplitude Distribution', fontsize=14)
    plt.xlabel('File Index (Sorted Order)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.ylabel('Amplitude Value', fontsize=12)
    plt.savefig("output.jpg")
    plt.show()


def main()->None:
    """
    Основная функция: чтение CSV → создание DataFrame → сортировка → график → сохранение.
    """
    parser = argparse.ArgumentParser(description='Process audio files and plot amplitude distribution')
    parser.add_argument('source', type=Path, help='Path to CSV file or directory')
    args = parser.parse_args()
    
    df = set_dataframe(args.source)
    
    sorted_df = sort_amplitudes(df)
    
    plot_sorted_min_amplitude(sorted_df)
    
    sorted_df.to_csv("audio_analysis.csv", index=False)
    print("DataFrame saved to audio_analysis.csv")

if __name__ == "__main__":
    main()




