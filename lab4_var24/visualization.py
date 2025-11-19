import matplotlib.pyplot as plt
import pandas as pd


def plot_amplitude_histogram(df, output_path='amplitude_histogram.png'):
    """
    Строит гистограмму распределения файлов по 5 диапазонам амплитуды
    """
    bins = [0.02, 0.07, 0.12, 0.17, 0.22, 0.25]
    range_names = ["0.02–0.07","0.07–0.12","0.12–0.17","0.17–0.22","0.22–0.25"]
    
    amp_range = pd.cut(df["amplitude"], bins=bins, labels=range_names, include_lowest=True)
    
    range_counts = amp_range.value_counts().sort_index()
    
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(range_counts)), range_counts.values, color='blue', edgecolor='black')
    plt.xlabel('Диапазон амплитуды', fontsize=12)
    plt.ylabel('Количество файлов', fontsize=12)
    plt.title('Распределение файлов по амплитуде', fontsize=14)
    plt.xticks(range(len(range_counts)), range_counts.index, rotation=45, ha='right')
    for i, v in enumerate(range_counts.values):
        plt.text(i, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    plt.show()
