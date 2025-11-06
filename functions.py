import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import soundfile as sf


class AudioTrack:
    """Class that reads and works with audio data"""

    def __init__(self, path):
        """Constructor. Accept path to music file"""
        if os.path.isfile(path):
            self.data, self.samplerate = sf.read(path)
            if self.data.ndim == 2:  # Преобразование стерео в моно с помощью усреднения
                self.data = np.mean(self.data, axis=1)
        else:
            raise FileNotFoundError("The file cannot be opened.")

    def get_samples(self) -> np.ndarray:
        """Return samples of current audio file"""
        return self.data


def calculate_ratio(samples: np.ndarray, threshold: float) -> float:
    """Returns the ratio of the number of samples below the threshold to the total number of them"""
    total_samples = len(samples)
    if total_samples == 0:
        return 0
    below_threshold = sum(1 for s in samples if abs(s) < threshold)
    return below_threshold / total_samples


def sort_by_ratio(df: pd.DataFrame) -> pd.DataFrame:
    """Sort DataFrame by ratio below threshold"""
    return df.sort_values(by="Ratio below threshold").reset_index(drop=True)


def filter_by_ratio(df: pd.DataFrame, value: float) -> pd.DataFrame:
    """Filter DataFrame by ratio below threshold for current value"""
    return df[df["Ratio below threshold"] > value].reset_index(drop=True)


def visualization(df: pd.DataFrame) -> None:
    """Show the graph of dataframe ratio and save it to png"""
    plt.figure(figsize=(12, 6))

    plt.plot(
        df.index,
        df["Ratio below threshold"],
        marker="o",
        linestyle="-",
        linewidth=1,
        markersize=3,
    )

    plt.xlabel("Номер аудиофайла в отсортированном списке")
    plt.ylabel("Отношение сэмплов ниже порога")
    plt.title("Отношение сэмплов ниже порога для аудиофайлов (отсортировано)")

    plt.grid(True, linestyle="--", alpha=0.7)

    plt.tight_layout()

    plt.savefig("audio_ratio_plot.png", dpi=300, bbox_inches="tight")
    plt.show()
