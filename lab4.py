import pandas as pd
import matplotlib.pyplot as plt
import soundfile as sf
import numpy as np
import argparse

def sort_by(df: pd.DataFrame, column: str, reverse: bool = False) -> pd.DataFrame:
    data = df.sort_values(by=column, ascending=not reverse)
    data.reset_index(drop=True, inplace=True)
    return data

def filter_by(df: pd.DataFrame, expression: str) -> pd.DataFrame:
    data = df.query(expression)
    data.reset_index(drop=True, inplace=True)
    return data

def count_samples_ratio(audio_path: str, min_amplitude: float) -> float:
    try:
        audio, samplerate = sf.read(audio_path)
        samples = np.where(np.abs(audio.flatten()) > min_amplitude)[0]
        return float(len(samples) / np.prod(audio.shape))
    except Exception as e:
        print(f"Ошибка обработки {audio_path}: {e}")
        return 0.0

def main(csv_path: str, output_frame: str, output_graph: str, min_amplitude: float) -> None:
    # Читаем аннотацию
    data = pd.read_csv(csv_path)
    
    # Переименовываем колонки
    if len(data.columns) >= 2:
        data.columns = ['absolute_path', 'relative_path'][:len(data.columns)]
    
    print("Первые 5 строк исходных данных:")
    print(data.head())
    print()

    data["amplitude_ratio"] = data['absolute_path'].apply(
        lambda x: count_samples_ratio(x, min_amplitude)
    )

    print("DataFrame с добавленной колонкой (первые 5 строк):")
    print(data.head())
    print()

    # Демонстрация фильтрации
    filtered = filter_by(data, "amplitude_ratio > 0.1")
    print(f"Найдено {len(filtered)} файлов с отношением > 0.1:")
    print(filtered[['relative_path', 'amplitude_ratio']].head())
    print()

    # Сортировка для графика
    data_sorted = sort_by(data, "amplitude_ratio")
    
    # Строим график
    plt.figure(figsize=(12, 6))
    plt.plot(data_sorted["amplitude_ratio"], marker='o', linewidth=2, markersize=4)
    plt.xlabel("Номер аудиофайла в отсортированном списке")
    plt.ylabel("Отношение сэмплов выше порога")
    plt.title("Анализ аудиоданных - отношение сэмплов с амплитудой выше порога")
    plt.grid(True, alpha=0.3)
    
    # Сохраняем график
    plt.savefig(output_graph, dpi=300, bbox_inches='tight')
    
    # Сохраняем DataFrame
    data.to_csv(output_frame, index=False)
    
    successful = sum(1 for x in data["amplitude_ratio"] if x > 0)
    print(f"Успешно обработано файлов: {successful}/{len(data)}")
    print(f"Результаты сохранены в файлы:")
    print(f"  - Данные: {output_frame}")
    print(f"  - График: {output_graph}")
    
    plt.show()
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--csv", type=str, 
                       help="Путь к файлу аннотации", 
                       default="annotation.csv")
    
    parser.add_argument("-of", "--output_frame", type=str, 
                       help="Путь для сохранения новых данных", 
                       default="audio_analysis_results.csv")
    
    parser.add_argument("-og", "--output_graph", type=str, 
                       help="Путь для сохранения графика", 
                       default="amplitude_ratio_plot.png")
    
    parser.add_argument("-min", "--min_amplitude", type=float, 
                       help="Порог амплитуды для подсчёта отношения", 
                       default=0.1)

    args = parser.parse_args()

    try:
        if 0 <= args.min_amplitude <= 1:
            main(args.csv, args.output_frame, args.output_graph, args.min_amplitude)
        else:
            raise ValueError("Значение --min_amplitude должно быть от 0 до 1!")
    except ValueError as e:
        print(f"Ошибка: {e}")
    except FileNotFoundError as e:
        print(f'Ошибка: не найден файл "{e.filename}"')
    except PermissionError as e:
        print(f"Ошибка прав доступа: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
