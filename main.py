import pandas
import matplotlib.pyplot as plt
import soundfile as sf
import numpy as np


def sort_by(df: pandas.DataFrame, column: str, reverse: bool = False) -> pandas.DataFrame:
    """
    Зачем-то в задании требуется реализовать функцию сортировки по новой колонке. Вот Вам сортировка по любой колонке.
    И да, это просто обёртка на встроенную готовую функцию в pandas
    Args:
        df (DataFrame): Данные для сортировки
        column (str): Колонка, по которой происходит сортировка
        reverse (boll): Прямой или обратный порядок сортировки
    """
    data = df.sort_values(by=column, ascending= not reverse)
    data.reset_index(drop = True, inplace=True)
    return data


def filter_by(df: pandas.DataFrame, expression: str) -> pandas.DataFrame:
    """
    У меня много вопрос касательно того, как будет происходить фильтрация значений, поэтому просто используйте выражение из pandas.
    Для числовых значений например: "column > 2"
    Args:
        df (DataFrame): Данные для фильтрации
        expression (str): Условное выражение для фильтрации.
    """
    data = df.query(expression)
    data.reset_index(drop = True, inplace=True)
    return data


def count_samples_ratio(audio_path: str, min_amplitude: float) -> float:
    """
    Вычисляет отношение всех сэмплов выше заданной амплитуды min_amplitude ко всем сэмплам аудиофайла.
    Args:
        audio_path (str): Путь до аудиофайла
        min_amplitude (float): Порог амплитуды, выше которого идёт подсчёт сэмплов
    """
    with open(f"{audio_path}", mode="rb") as f:
        audio, samplerate = sf.read(f)
    samples = np.where(np.abs(audio.flatten()) > min_amplitude)[0]
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

    # print(data.query("ratio > 0.1")) не пригодилось
    
    data = sort_by(data, "ratio")
    plt.plot(data["ratio"])
    plt.xlabel("Индекс аудиофайла")
    plt.ylabel("Отношение")
    plt.savefig(output_graph)
    data.to_csv(output_frame, index=False)
    plt.show()
    plt.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--csv", type=str, help="Путь к файлу аннотации", default="downloads/annotation.csv")
    parser.add_argument("-of", "--output_frame", type=str, help="Путь для сохранения новых данных", default="downloads/output.csv")
    parser.add_argument("-og", "--output_graph", type=str, help="Путь для сохранения графика", default="downloads/output.png")
    parser.add_argument("-min", "--min_amplitude", type=float, help="Значение минимальный амплитуды для подсчёта отношения", default=0.5)
    args = parser.parse_args()

    try:
        if 0 <= args.min_amplitude <= 1:
            main(args.csv, args.output_frame, args.output_graph, args.min_amplitude)
        else:
            raise ValueError("Значение --min_amplitude должно быть в пределах от 0 до 1!")
    except ValueError as e:
        print(f"Ошибка: {e}")
    except FileNotFoundError as e:
        print(f'Ошибка, не найден файл: "{e.filename}"')
    except PermissionError as e:
        print(f"Недостаточно прав для совершения операции: {e}")