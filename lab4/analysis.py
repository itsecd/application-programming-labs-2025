import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from audio_mixer import AudioMixer


def get_args() -> argparse.Namespace:
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--annotation', type=str, default='ann.csv', 
                       help='Путь к CSV файлу с аннотацией')
    parser.add_argument('--output_df', type=str, default='audio_analysis.csv',
                       help='Путь для сохранения DataFrame')
    parser.add_argument('--output_plot', type=str, default='amplitude_plot.png',
                       help='Путь для сохранения графика')
    return parser.parse_args()


def build_dataframe(annotation_file: str) -> pd.DataFrame:
    """Создание DataFrame с путями и амплитудами"""
    df_annotation = pd.read_csv(annotation_file)
 
    df = pd.DataFrame({
        'абсолютный_путь': df_annotation['Абсолютный путь'],
        'относительный_путь': df_annotation['Относительный путь']
    })
    
    mixer = AudioMixer()
    amplitudes = []
    
    for audio_path in df['абсолютный_путь']:
        try:
            audio_data, _ = mixer.read_audio_file(audio_path)
            if audio_data is not None:
                mean_amp = np.mean(np.abs(audio_data))
                amplitudes.append(mean_amp)
            else:
                amplitudes.append(0.0)
        except Exception:
            amplitudes.append(0.0)
    
    df['средняя_амплитуда'] = amplitudes
    
    return df


def sort_dataframe(df: pd.DataFrame, column: str = 'средняя_амплитуда', 
                   ascending: bool = True) -> pd.DataFrame:
    """Сортировка DataFrame по указанной колонке"""
    return df.sort_values(column, ascending=ascending).reset_index(drop=True)


def filter_dataframe(df: pd.DataFrame, column: str = 'средняя_амплитуда', 
                     min_value: float = None, max_value: float = None) -> pd.DataFrame:
    """Фильтрация DataFrame по диапазону значений"""
    filtered_df = df.copy()
    
    if min_value is not None:
        filtered_df = filtered_df[filtered_df[column] >= min_value]
    if max_value is not None:
        filtered_df = filtered_df[filtered_df[column] <= max_value]
    
    return filtered_df.reset_index(drop=True)

def save_dataframe(df: pd.DataFrame, filepath: str) -> None:
    """Сохранение DataFrame в файл"""
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"DataFrame сохранен: {filepath}")


def plot_amplitudes(df: pd.DataFrame, output_path: str) -> None:
    """Построение графика средней амплитуды"""
    plt.figure(figsize=(12, 6))
    
    plt.plot(range(len(df)), df['средняя_амплитуда'])
    
    plt.title('Средняя амплитуда аудиофайлов (отсортированные)', fontsize=14)
    plt.xlabel('Номер аудиофайла в отсортированном списке', fontsize=12)
    plt.ylabel('Средняя амплитуда', fontsize=12)
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.show()
    print(f"График сохранен: {output_path}")