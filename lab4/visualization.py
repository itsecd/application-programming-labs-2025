import matplotlib.pyplot as plt
import pandas as pd


def plot_amplitude(df: pd.DataFrame, out_path: str):
    """
    Строит график минимальной амплитуды
    всех файлов из директории.
    X - номер файла в отсортированном DataFrame.
    Y - мин. амплитуда сигнала.
    """

    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["min_amplitude"], marker='o')
    plt.xlabel("Номер аудиофайла")
    plt.ylabel("Минимальная амплитуда")
    plt.title("Минимальная амплитуда аудиофайлов")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
