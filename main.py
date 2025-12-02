from typing import Optional
import pandas as pd
import argparse
import numpy as np
from pathlib import Path
import soundfile as fs
import matplotlib.pyplot as plt


def get_two_first_columns(csv_path: Path) -> Optional[pd.DataFrame]:
    """
    Формирование DataFrame с первыми двумя столбцами из .csv файла.
    """

    csv_path = Path(csv_path)

    if csv_path.exists():
        df = pd.read_csv(csv_path)

        if df.shape[1] < 2:
            print(f".csv file doesn't have two columns")
            return None

        new_df = df.iloc[:, 0:2]
        print(f"Two first columns saved")
        return new_df
    
    else:
        print(f"File does not exist")
        return None


def new_columns_names(data_frame: pd.DataFrame) -> None:
    """
    Переименование столбцов.
    """

    data_frame.columns = ['Absolute path', 'Relative path']
    print(f'Columns names changed to \'Absolute path\' and \'Relative path\'')
    return data_frame


def average_amplitude(x: pd.Series) -> float:
    """
    Вычисление средней амплитуды.
    """

    audio_path = x["Absolute path"]
    data, samplerate = fs.read(audio_path)

    if data.ndim == 2:
        mono_data = np.mean(data, axis = 1)
    else:
        mono_data = data

    average_amplitude = np.mean(np.abs(mono_data))
    return round(average_amplitude, 2)


def average_amplitude_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Создание отдельного столбца со средними значениями амплитуд.
    """

    df["Average amplitude"] = df.apply(average_amplitude, axis = 1)
    print(f"Created a new column: \'Average amplitude\'")
    return df


def sort_data_frame(df: pd.DataFrame) -> pd.DataFrame:
    """
    Сортировка DataFrame по значениям последнего столбца по возрастанию.
    """

    sorted_df = df.sort_values(["Average amplitude"], ascending = True)
    sorted_df = sorted_df.reset_index(drop=True)
    print(f"Data frame now is sorted")
    print(f"Range: {df['Average amplitude'].min():.4f} - {df['Average amplitude'].max():.4f}")
    return sorted_df


def filter_data_frame(df: pd.DataFrame) -> pd.DataFrame:
    """
    Фильтрация DataFrame, остаются те строки, амплитуда которых больше 20.
    """

    filtered_df = df[df["Average amplitude"] >= 0.05]
    filtered_df = filtered_df.reset_index(drop=True)
    print(f"Data frame now is filtered")
    print(f"Left {len(filtered_df)} rows")
    return filtered_df


def plot_sorted_amplitudes(df: pd.DataFrame) -> None:
    """
    Построение графика средних амплитуд по DataFrame и сохранение графика в файл.
    """
    
    x = np.arange(0, len(df))
    y = df["Average amplitude"].values
    y_max = y.max() * 1.1
    y_min = y.min() * 0.9

    plt.figure(figsize=(10, 5))
    
    plt.plot(x, y, marker='o', linestyle='-', linewidth=0.5, color='blue')
    plt.title('Average amplitudes graphic')
    plt.xlabel('The index of the audio')
    plt.ylabel('Average amplitude')
    plt.axhline(0, color='black',linewidth=0.5, ls='--')
    plt.axvline(0, color='black',linewidth=0.5, ls='--')
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    plt.legend()
    plt.ylim([y_min, y_max])
    plt.tight_layout()

    filename = f"Average_amplitudes_graphic.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')

    plt.show()
    print(f"Graphic saved as {filename}")
    return None


def save_dataframe(df: pd.DataFrame, csv_path: Path) -> None:
    """
    Сохранение DataFrame в .csv файле.
    """
    
    csv_path = Path(csv_path)
    df.to_csv(csv_path, index=False)
    print(f"Data Frame saved in the {csv_path}")
    return None


def main():
    parser = argparse.ArgumentParser(description = "Average amplitude for each audio file")
    parser.add_argument('input_file', type = str, help = "path to the annotation file")
    parser.add_argument('output_file', type = str, help = "path where to save new file")
    args = parser.parse_args()

    data_frame = get_two_first_columns(args.input_file)
    data_frame = new_columns_names(data_frame)
    data_frame = average_amplitude_column(data_frame)
    data_frame = filter_data_frame(data_frame)
    data_frame = sort_data_frame(data_frame)
    save_dataframe(data_frame, args.output_file)
    plot_sorted_amplitudes(data_frame)


if __name__ == "__main__":
    main()