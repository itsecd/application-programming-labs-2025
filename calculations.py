import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import librosa as ls


def dataframe_read(csv_path: str) -> pd.DataFrame:
    """
    Загружает датафрейм из CSV, и берёт две последние колонки (пути)
    """
    try:
        df = pd.read_csv(csv_path)
        df = df.iloc[:, -2:]
        df["min_amp"] = 0.0
        return df
    except FileNotFoundError:
        print(f"Файл {csv_path} не найден")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def calc_min_amp(filename: str) -> float:
    """
    Возвращает значение минимальной амплитуды
    """
    try:
        y, sr = ls.load(filename, mono=True)
        min_amp = np.min(np.abs(y))
        return min_amp
    except Exception as e:
        print(f"Ошибка при обработке {filename}: {e}")


def create_min_amp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Создаёт датафрейм и добавляет минимальную амплитуду и сортирует min_amp
    """
    for index, row in df.iterrows():
        filename = row["absolute_path"]
        min_amp = calc_min_amp(filename)
        df.loc[index, "min_amp"] = min_amp
    df = df.sort_values("min_amp")
    df = df.reset_index(drop=True)
    return df


def filtration_df(df: pd.DataFrame, val: float) -> pd.DataFrame:
    filtered_df = df[df["min_amp"] == val]
    return filtered_df


def save_df(df: pd.DataFrame, output_path: str) -> None:
    """
    Сохраняет датафрейм в csv файл
    """
    df.to_csv(f"{output_path}.csv")
    print(f"Датафрейм сохранён в {output_path}.csv")


def create_chart(df: pd.DataFrame, output_path: str) -> None:
    """
    Построение графика для распределения
    """

    x = np.arange(len(df))
    y = df["min_amp"].values

    plt.figure(figsize=(12, 6))
    plt.plot(x, y, linewidth=2, color="blue", marker="o", markersize=4)

    plt.title("Минимальная амплитуда звука по файлам")
    plt.xlabel("Номер файла (отсортированный список)")
    plt.ylabel("Минимальная амплитуда")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{output_path}.png", dpi=300)
    print(f"График сохранен в {output_path}.png")
    plt.show()
