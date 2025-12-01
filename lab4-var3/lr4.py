import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import os

# Пути к файлам
input_csv = "/Users/mera/Documents/tuition/3semester/AD/application-programming-labs-2025/lab2-var3/fish_annotation.csv"
output_csv = "/Users/mera/Documents/tuition/3semester/AD/application-programming-labs-2025/lab4-var3/lab4_output.csv"
plot_file = "/Users/mera/Documents/tuition/3semester/AD/application-programming-labs-2025/lab4-var3/area_plot.png"

# Чтение исходного CSV
df = pd.read_csv(input_csv)

# Оформляем DataFrame с абсолютными и относительными путями
df_clean = pd.DataFrame({
    "Абсолютный путь": df['absolute_path'].astype(str).str.strip(),
    "Относительный путь": df['relative_path'].astype(str).str.strip()
})

# Функция для вычисления площади изображения
def вычислить_площадь(path):
    try:
        with Image.open(path) as img:
            return img.width * img.height
    except:
        return 0

# Добавляем колонку с площадью
df_clean["Площадь"] = df_clean["Абсолютный путь"].apply(вычислить_площадь)

# Функция сортировки по площади
def сортировать_по_площади(df):
    return df.sort_values(by="Площадь").reset_index(drop=True)

# Функция фильтрации по площади (оставляем только >0)
def фильтровать_по_площади(df):
    return df[df["Площадь"] > 0].reset_index(drop=True)

# Применяем сортировку и фильтрацию
df_sorted = сортировать_по_площади(df_clean)
df_filtered = фильтровать_по_площади(df_sorted)

# Сохраняем DataFrame в CSV
df_filtered.to_csv(output_csv, index=False)

# Строим график
plt.figure(figsize=(8,5))
plt.plot(range(1, len(df_filtered)+1), df_filtered["Площадь"], marker='o')
plt.xlabel("Номер изображения в отсортированном списке")
plt.ylabel("Площадь (px²)")
plt.title("Площади изображений")
plt.grid(True)
plt.tight_layout()
plt.savefig(plot_file)
plt.show()