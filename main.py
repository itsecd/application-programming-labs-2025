import soundfile as fs
import matplotlib.pyplot as plt
import argparse
import os
import csv
import random
from pathlib import Path
import numpy as np
import pandas as pd

def get_two_audio_paths(csv_path, rows_indexes):
    csv_path = Path(csv_path)

    if csv_path.exists():
        df = pd.read_csv(csv_path)
        first_ind, second_ind = rows_indexes

        if first_ind < len(df) and second_ind < len(df):
            audio_paths = df.iloc[rows_indexes, 0]
            print(f"audio_paths")
            return audio_paths
        else:
            print(f"These indexes are not valid")
            return None
    else:
        print(f"File with this path no exists")
        return None


def merge_two_audio(audio_paths, output_path):
    data1, samplerate1 = fs.read(audio_paths.iloc[0])
    data2, samplerate2 = fs.read(audio_paths.iloc[1])

    if len(data1) != len(data2):
            if len(data1) > len(data2):
                if data2.ndim == 1:
                    data2 = np.pad(data2, (0, len(data1) - len(data2)), 'constant')
                else:
                    padding = np.zeros((len(data1) - len(data2), data2.shape[1]))
                    data2 = np.vstack([data2, padding])

            else:
                if data1.ndim == 1:
                    data1 = np.pad(data1, (0, len(data2) - len(data1)), 'constant')
                else:
                    padding = np.zeros((len(data2) - len(data1), data1.shape[1]))
                    data1 = np.vstack([data1, padding])

    samplerate = samplerate1

    if data1.ndim == 1 and data2.ndim == 2:
        data1_stereo = np.column_stack([data1, data1])
        merge_data = data1_stereo + data2

    elif data1.ndim == 2 and data2.ndim == 1:
        data2_stereo = np.column_stack([data2, data2])
        merge_data = data1 + data2_stereo

    else:
        merge_data = data1 + data2

    fs.write(output_path, merge_data, samplerate)
    return None



def main():
    parser = argparse.ArgumentParser(description = "Merge of 2 audio files")
    parser.add_argument('input_file', type = str, help = "path to the annotation file")
    parser.add_argument('output_file', type = str, help = "name of the new file")
    parser.add_argument('--first_audio', '-f', type = int, help = "index of the first audio from 0 to 13")
    parser.add_argument('--second_audio', '-s',  type = int, help = "index of the second audio from 0 to 13")
    args = parser.parse_args()

    if args.first_audio is None:
        args.first_audio = random.randint(0, 13)
    if args.second_audio is None:
        args.second_audio = random.randint(0, 13)

    audio_indexes = [args.first_audio, args.second_audio]
    audio_paths = get_two_audio_paths(args.input_file, audio_indexes)
    merge_two_audio(audio_paths, args.output_file)


if __name__ == "__main__":
    main()
