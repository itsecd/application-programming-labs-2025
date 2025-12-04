import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import wave


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
        raise FileExistsError(f"Файл {csv_path} не найден")
    except Exception as e:
        raise e(f"Произошла ошибка: {e}")


def calc_max_amp(filename: str) -> float:
    """Только для WAV файлов"""
    with wave.open(filename, "rb") as wf:
        frames = wf.readframes(wf.getnframes())
        samples = np.frombuffer(frames, dtype=np.int16)
        return np.max(np.abs(samples)) / 32768.0


def assign_amp_range(value: float) -> str:
    """
    Присваивает диапазон амплитуды по заданным интервалам
    """
    bins = [0, 0.1, 0.2, 0.4, 0.6, 1.0]
    labels = ["0-0.1", "0.1-0.2", "0.2-0.4", "0.4-0.6", "0.6-1.0"]
    for i in range(len(bins) - 1):
        if bins[i] <= value < bins[i + 1]:
            return labels[i]
    return labels[-1]


def create_max_amp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавляет колонку максимальной амплитуды и диапазонов
    """
    df["max_amp"] = df["absolute_path"].apply(calc_max_amp)
    df["amp_range"] = df["max_amp"].apply(assign_amp_range)
    return df


def sort_by_amp_range(df: pd.DataFrame) -> pd.DataFrame:
    """
    Сортирует датафрейм по диапазону амплитуды
    """
    order = ["0-0.1", "0.1-0.2", "0.2-0.4", "0.4-0.6", "0.6-1.0"]
    df["amp_range"] = pd.Categorical(df["amp_range"], categories=order, ordered=True)
    return df.sort_values("amp_range").reset_index(drop=True)


def filter_by_amp_range(df: pd.DataFrame, amp_range: str) -> pd.DataFrame:
    """
    Фильтрует датафрейм по диапазону амплитуды
    """
    return df[df["amp_range"] == amp_range]


def save_df(df: pd.DataFrame, output_path: str) -> None:
    """
    Сохраняет датафрейм в CSV
    """
    df.to_csv(f"{output_path}.csv", index=False)
    print(f"Датафрейм сохранен в {output_path}.csv")


def create_chart(df: pd.DataFrame, output_path: str) -> None:
    """
    Отображает и сохраняет гистограмму распределения амплитудных диапазонов
    """
    counts = df["amp_range"].value_counts().sort_index()

    plt.figure(figsize=(8, 5))
    counts.plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title("Распределение файлов по диапазонам максимальной амплитуды")
    plt.xlabel("Диапазон максимальной амплитуды")
    plt.ylabel("Количество файлов")
    plt.xticks(rotation=45)
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{output_path}.png", dpi=300)
    print(f"Гистограмма сохранена в {output_path}.png")
    plt.show()
