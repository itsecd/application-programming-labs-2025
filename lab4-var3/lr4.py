import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import os

input_csv = "/Users/mera/Documents/tuition/3semester/AD/application-programming-labs-2025/lab2-var3/fish_annotation.csv"
output_csv = "/Users/mera/Documents/tuition/3semester/AD/application-programming-labs-2025/lab4-var3/lab3_output.csv"
plot_file = "/Users/mera/Documents/tuition/3semester/AD/application-programming-labs-2025/lab4-var3/area_plot.png"

df = pd.read_csv(input_csv)
df['absolute_path'] = df['absolute_path'].astype(str).str.strip()

def get_area(path):
    try:
        with Image.open(path) as img:
            return img.width * img.height
    except:
        return 0

df['Area'] = df['absolute_path'].apply(get_area)
df_sorted = df.sort_values(by='Area').reset_index(drop=True)
df_filtered = df_sorted[df_sorted['Area'] > 0].reset_index(drop=True)

df_filtered.to_csv(output_csv, index=False)

plt.figure(figsize=(10, 6))
plt.plot(range(1, len(df_filtered) + 1), df_filtered['Area'], marker='o')
plt.xlabel("Image Index (sorted)")
plt.ylabel("Area")
plt.title("Image Areas")
plt.grid(True)
plt.savefig(plot_file)
plt.show()