import pandas as pd
import matplotlib.pyplot as plt


def creating_graph_and_save(df: pd.DataFrame, fail_save_chart: str) -> None:
    """
    функция для отрисовки графика и сохранения
    """
    x = range(len(df))
    plt.figure(figsize=(10, 6))
    plt.plot(x, df["range_r"], color="red", label="Красный канал")
    plt.plot(x, df["range_g"], color="green", label="Зелёный канал")
    plt.plot(x, df["range_b"], color="blue", label="Синий канал")
    plt.xlabel("Номер изображения")
    plt.ylabel("Диапазон яркости (max - min)")
    plt.legend()
    plt.grid(True)
    plt.savefig(fail_save_chart)
    plt.show()
