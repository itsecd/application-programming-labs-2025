import pandas
import matplotlib.pyplot as plt
import soundfile as sf
import numpy as np
import argparse

def sort_by(df: pandas.DataFrame, column: str, reverse: bool = False) -> pandas.DataFrame:
    """
    Сортирует DataFrame по указанной колонке.

    Аргументы:
        df (pandas.DataFrame): Таблица данных для сортировки.
        column (str): Название колонки, по которой выполняется сортировка.
        reverse (bool): Если True — сортировка по убыванию.
                        Если False — по возрастанию.
    """
    data = df.sort_values(by=column, ascending=not reverse)
    data.reset_index(drop=True, inplace=True)
    return data

def filter_by(df: pandas.DataFrame, expression: str) -> pandas.DataFrame:
    """
    Фильтрует DataFrame, используя выражение формата pandas.query().

    Аргументы:
        df (pandas.DataFrame): Таблица данных для фильтрации.
        expression (str): Условие фильтрации, например:
                          "min_amp > 0.01" или "min_amp_range == '0–0.01'".
    """
    data = df.query(expression)
    data.reset_index(drop=True, inplace=True)
    return data

def get_min_abs_amplitude(audio_path: str) -> float:
    """
    Вычисляет минимальную амплитуду по модулю для аудиофайла.

    Аргументы:
        audio_path (str): Абсолютный путь до аудиофайла.
    """
    with open(audio_path, mode="rb") as f:
        audio, samplerate = sf.read(f)
    audio = np.asarray(audio).flatten()
    return float(np.min(np.abs(audio)))

def load_data(csv_path: str) -> pandas.DataFrame:
    """
    Загружает CSV-файл аннотаций в DataFrame.
    """
    return pandas.read_csv(csv_path)

def compute_min_amp_column(data: pandas.DataFrame) -> pandas.DataFrame:
    """
    Вычисляет минимальную абсолютную амплитуду (min |амплитуды|)
    для каждого аудиофайла и добавляет колонку 'min_amp'.

    Требования:
        DataFrame должен содержать колонку 'abs_path'.
    """
    min_amp_values = []
    for path in data["abs_path"]:
        min_amp_values.append(get_min_abs_amplitude(path))

    data["min_amp"] = min_amp_values
    return data

def add_histogram_bins(data: pandas.DataFrame) -> pandas.DataFrame:
    """
    Добавляет категориальные диапазоны (bins) для построения гистограммы
    на основе значений 'min_amp'.
    """
    bins = [0.0, 0.01, 0.02, 0.05, 0.1, 1.0]
    labels = ["0–0.01", "0.01–0.02", "0.02–0.05", "0.05–0.1", ">0.1"]
    data["min_amp_range"] = pandas.cut(data["min_amp"], bins=bins, labels=labels, include_lowest=True)
    return data

def plot_min_amp_histogram(data: pandas.DataFrame, output_graph: str) -> None:
    """
    Строит и сохраняет гистограмму распределения минимальной амплитуды.
    """
    counts = data["min_amp_range"].value_counts().sort_index()

    plt.figure(figsize=(6, 4))
    counts.plot(kind="bar")
    plt.xlabel("Диапазон минимальной амплитуды (|A_min|)")
    plt.ylabel("Количество файлов")
    plt.title("Гистограмма распределения минимальной амплитуды (по модулю)")
    plt.tight_layout()
    plt.savefig(output_graph)
    plt.show()
    plt.close()

def save_dataframe(data: pandas.DataFrame, output_frame: str) -> None:
    """
    Сохраняет датафрейм в CSV.
    """
    data.to_csv(output_frame, index=False)


def main(csv_path: str, output_frame: str, output_graph: str) -> None:
    """
    Основная логика:
    - читаем аннотацию,
    - считаем минимальную амплитуду по модулю,
    - добавляем колонки для гистограммы,
    - сортируем,
    - строим гистограмму,
    - сохраняем результат.
    """
    data = load_data(csv_path)
    data = compute_min_amp_column(data)
    data = add_histogram_bins(data)
    data = sort_by(data, "min_amp")
    plot_min_amp_histogram(data, output_graph)
    save_dataframe(data, output_frame)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--csv", type=str, help="Путь к файлу аннотации")
    parser.add_argument("-of", "--output_frame", type=str, help="Путь для сохранения новых данных")
    parser.add_argument("-og", "--output_graph", type=str, help="Путь для сохранения графика")

    args = parser.parse_args()

    try:
        main(args.csv, args.output_frame, args.output_graph)
    except FileNotFoundError as e:
        print(f'Ошибка, не найден файл: "{e.filename}"')
    except PermissionError as e:
        print(f"Недостаточно прав для совершения операции: {e}")