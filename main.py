import pandas
import matplotlib as plt
import soundfile as sf
import numpy as np

def count_samples_ratio(audio_path: str, min_amplitude: float) -> float:
    """
    Вычисляет отношение всех сэмплов выше заданной амплитуды min_amplitude ко всем сэмплам аудиофайла.
    Args:
        audio_path (str): Путь до аудиофайла
        min_amplitude (float): Порог амплитуды, выше которого идёт подсчёт сэмплов
    """
    with open(f"{audio_path}", mode="rb") as f:
        audio, samplerate = sf.read(f)
    samples = np.where(audio.flatten() > min_amplitude)[0]
    return float(len(samples) / np.prod(audio.shape))

def main(csv_path: str, output_frame: str, output_graph: str, min_amplitude: float) -> None:
    """ 
    Основная логика программы 
    Args:
        csv_path (str): Файл для аннотаций на загруженные файлы
        output_frame (str): Путь для сохранения новых данных
        output_graph (str): Путь для сохранения графика
        min_amplitude (float): Минимальная амплитуда сэмпла для подсчёта отношения
    """
    data = pandas.read_csv(csv_path)

    ratio_values = list()
    for path in data.iloc[:, 1]:
        ratio_values.append(count_samples_ratio(path, min_amplitude))

    data["ratio"] = ratio_values
    print(data)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--csv", type=str, help="Путь к файлу аннотации", default="downloads/annotation.csv")
    parser.add_argument("-of", "--output_frame", type=str, help="Путь для сохранения новых данных", default="downloads/output.csv")
    parser.add_argument("-og", "--output_graph", type=str, help="Путь для сохранения графика", default="downloads/output.png")
    parser.add_argument("-min", "--min_amplitude", type=float, help="Путь для сохранения графика", default=0)
    args = parser.parse_args()

    try:
        main(args.csv, args.output_frame, args.output_graph, args.min_amplitude)
    except FileNotFoundError as e:
        print(f'Ошибка, не найден файл: "{e.filename}"')
    except PermissionError as e:
        print(f"Недостаточно прав для совершения операции: {e}")