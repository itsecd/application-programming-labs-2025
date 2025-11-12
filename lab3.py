import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import argparse

def show_plots(original_audio: np.ndarray, combined_audio: np.ndarray) -> None:
    """
    Функция для отображения графиков исходного и объединенного аудио.
    """
    plt.figure(figsize=(10,6))

    plt.subplot(2, 1, 1)
    plt.plot(original_audio)
    plt.title("Исходный звук")
    plt.xlabel("Мелодия")
    plt.ylabel("Амплитуда")

    plt.subplot(2, 1, 2)
    plt.plot(combined_audio)
    plt.title("Объединенный звук")
    plt.xlabel("Мелодия")
    plt.ylabel("Амплитуда")

    plt.tight_layout()
    plt.show()

def main(file1: str, file2: str, output_file: str) -> None:
    """
    Основная функция для объединения двух аудиофайлов и отображения графиков.

    Args:
        file1 (str): Путь к первому аудиофайлу.
        file2 (str): Путь ко второму аудиофайлу.
        output_file (str): Путь для сохранения результата объединенного аудиофайла.
    
    Returns:
        None
    """

    audio1, sr1 = sf.read(file1)
    audio2, sr2 = sf.read(file2)
    
    if sr1 != sr2:
        print("астоты дискретизации двух файлов должны совпадать!")
        return
    combined_audio = np.concatenate((audio1, audio2))

    sf.write(output_file, combined_audio, sr1)

    show_plots(audio1, combined_audio)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f1", "--file1", type=str, required=True, help="Путь к первому аудиофайлу")
    parser.add_argument("-f2", "--file2", type=str, required=True, help="Путь ко второму аудиофайлу")
    parser.add_argument("-o", "--output", default="combined_audio.mp3", type=str, help="Путь для сохранения результата")

    args = parser.parse_args()

    try:
        main(args.file1, args.file2, args.output)
    except Exception as e:
        print(f"Произошла ошибка: {e}")