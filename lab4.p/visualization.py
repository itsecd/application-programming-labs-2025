from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def plot_orientation_histogram(
    df: pd.DataFrame,
    col: str = "orientation",
    output_path: str | Path = "orientation_hist.png",
) -> None:
    """Построить гистограмму ориентаций."""
    counts = df.dropna(subset=[col])[col].value_counts()

    plt.figure()
    plt.bar(counts.index, counts.values)
    plt.xlabel("Ориентация")
    plt.ylabel("Количество")
    plt.title("Распределение ориентаций")
    plt.tight_layout()

    plt.savefig(Path(output_path))
    plt.show()
