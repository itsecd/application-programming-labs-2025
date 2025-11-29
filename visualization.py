import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_brightness_data(df: pd.DataFrame, output_file: str) -> None:
    """
    Построение графика средних значений яркости по каналам R, G, B
    :param df: Обработанный DataFrame
    :param output_file: Путь для сохранения графика
    """
    plt.figure()

    x_indices = np.arange(len(df))

    plt.plot(x_indices, df["R"], label='Средняя яркость R-канала', color='red')
    plt.plot(x_indices, df["G"], label='Средняя яркость G-канала', color='green')
    plt.plot(x_indices, df["B"], label='Средняя яркость B-канала', color='blue')

    plt.title('График средних значений яркости по каждому каналу')
    plt.xlabel('Номер изображения')
    plt.ylabel('Среднее значение яркости')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.savefig(output_file)
    plt.show()
