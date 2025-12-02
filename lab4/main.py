import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd


def args_parse() -> argparse.Namespace:
    """Данная функция получает аргументы из командной строки"""
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--annotation_path', help='Путь до файла аннотации')
    parser.add_argument('-o_graph', '--output_graph_path', help='Путь для сохранения графика')
    parser.add_argument('-o_df', '--output_df_path', help='Путь для сохранения DataFrame')

    args = parser.parse_args()

    if (args.output_graph_path is None) or (args.output_df_path is None) or (args.annotation_path is None):
        raise Exception("Incorrectly passed arguments")
    
    return args


def get_channel_brightness(image_path: str) -> tuple[float, float, float]:
    """Эта функция получает средние значения яркости по каналам"""
    img = cv2.imread(image_path)
    
    if img is None:
        raise FileNotFoundError("Image not found")

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    r_avg = np.mean(img_rgb[:, :, 0])
    g_avg = np.mean(img_rgb[:, :, 1])
    b_avg = np.mean(img_rgb[:, :, 2])

    return (r_avg, g_avg, b_avg)


def add_brightness_columns(df: pd.DataFrame) -> None:
    """Эта функция добавляет  колонки со средними значениями яркости по каждому каналу (r, g, b) изображения"""
    df['r_avg'] = None
    df['g_avg'] = None
    df['b_avg'] = None

    for i in range(0, len(df)):
        r_avg, g_avg, b_avg = get_channel_brightness(df['absolute_path'][i])
        df.loc[i, 'r_avg'] = r_avg
        df.loc[i, 'g_avg'] = g_avg
        df.loc[i, 'b_avg'] = b_avg
        

def sort_by_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Данная функция возвращает отсортированный по столбцам DataFrame"""
    return df.sort_values(by=['r_avg', 'g_avg', 'b_avg']).reset_index(drop=True)


def filtered_by_columns(df: pd.DataFrame, 
                        r_avg_min: float,
                        g_avg_min: float, 
                        b_avg_min: float) -> pd.DataFrame:
    "Данная функция фильтрует DataFrame по минимальным значениям r_avg, g_avg, b_avg"
    df_filtered = df.copy()

    mask = (df_filtered['r_avg'] >= r_avg_min) & (df_filtered['g_avg'] >= g_avg_min) & (df_filtered['b_avg'] >= b_avg_min)

    return df_filtered[mask].reset_index(drop=True)


def save_graph(sorted_df: pd.DataFrame, path: str) -> None:
    """
    Данная функция строит график по средним значения яркости
    по каждому каналу (r, g, b), а затем сохраняет его 
    по указанному пути
    """
    plt.figure(figsize=(12, 6))

    plt.plot(
        range(len(sorted_df)),
        sorted_df['r_avg'],
        color='red',
        marker='o',
        linestyle='-',
        linewidth=1,
        markersize=3,
        alpha=0.7,
        label='Красный канал (R)'
    )
    
    plt.plot(
        range(len(sorted_df)),
        sorted_df['g_avg'],
        color='green',
        marker='o',
        linestyle='-',
        linewidth=1,
        markersize=3,
        alpha=0.7,
        label='Зелёный канал (G)'
    )

    plt.plot(
        range(len(sorted_df)),
        sorted_df['b_avg'],
        color='blue',
        marker='o',
        linestyle='-',
        linewidth=1,
        markersize=3,
        alpha=0.7,
        label='Синий канал (B)'
    )
    
    plt.title(
        'Средняя яркость по каналам RGB для отсортированных изображений',
        fontsize=14
        )

    plt.xlabel('Номер изображения в отсортированном списке', fontsize=12)
    plt.ylabel('Средняя яркость', fontsize=12)
    
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()


def save_df(df: pd.DataFrame, path: str) -> None:
    """Данная функция сохраняет DataFrame по указанному пути"""
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    df.to_csv(path, index=False)


def main() -> None: 
    arguments = args_parse()

    annotation_file = arguments.annotation_path
    output_graph_path = arguments.output_graph_path
    output_df_path = arguments.output_df_path

    df = pd.read_csv(annotation_file)
    df.columns = ["absolute_path", "relative_path"]
    add_brightness_columns(df)
    df = sort_by_columns(df)
    
    print(filtered_by_columns(df, 110, 131, 11))

    save_graph(df, output_graph_path)
    save_df(df, output_df_path)


if __name__ == "__main__":
    main()