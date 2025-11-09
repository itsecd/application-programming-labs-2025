import numpy
import cv2
import pandas as pd


def rang_calculate(path: str) -> int:
    img = cv2.imread(path)
    height, width, channels = img.shape
    max=-1
    min=256
    for i in range(height):
        for j in range(width):
            for k in range(3):
                if max<img[i,j,k]:
                    max = img[i,j,k]
                if min>img[i,j,k]:
                    min = img[i,j,k]
    return max-min

def sort_by_brightness_range(df: pd.DataFrame):
    """Sort DataFrame by brightness range"""
    return df.sort_values(by="brightness range")

def filter_by_brightness_range(df: pd.DataFrame, value: int):
    """Filter DataFrame by brightnessrange"""
    return df[df["brightness range"] > value].reset_index(drop=True)



def main():
    df = pd.read_csv("annotation.csv")
    df['brightness range'] = 0
    for i in range(len(df)):
        df.iloc[i,2] = rang_calculate(df.iloc[i,1])
    df = sort_by_brightness_range(df)
    df = filter_by_brightness_range(df, 250)
    print(df)

if __name__ == "__main__":
    main()