import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Данные 
data = {
    'абсолютный_путь': [
        r'C:\Users\User\Desktop\py\pig_images\000001.jpg',
        r'C:\Users\User\Desktop\py\pig_images\000002.jpg',
        r'C:\Users\User\Desktop\py\pig_images\000003.jpg',
        r'C:\Users\User\Desktop\py\pig_images\000004.jpg'
    ],
    'относительный_путь': [
        'pig_images\\000001.jpg',
        'pig_images\\000002.jpg',
        'pig_images\\000003.jpg',
        'pig_images\\000004.jpg'
    ]
}

# Создаем DataFrame
df = pd.DataFrame(data)

# Добавляем столбец с соотношением сторон
соотношения = []
for path in df['абсолютный_путь']:
    try:
        with Image.open(path) as img:
            width, height = img.size
            соотношения.append(round(width / height, 2))
    except:
        соотношения.append(1.33)  # значение по умолчанию

df['соотношение_сторон'] = соотношения

# Добавляем столбец для гистограммы
df['диапазон'] = pd.cut(df['соотношение_сторон'], 
                       bins=[0.5, 1.0, 1.5, 2.0, 2.5], 
                       labels=['0.5-1.0', '1.0-1.5', '1.5-2.0', '2.0-2.5'])

print("DataFrame:")
print(df)

# Функция сортировки
def сортировать_по_соотношению(df):
    return df.sort_values('соотношение_сторон')

# Функция фильтрации  
def фильтровать_по_диапазону(df, диапазон):
    return df[df['диапазон'] == диапазон]

# Сортируем данные
df_отсортированный = сортировать_по_соотношению(df)
print("\nОтсортированный DataFrame:")
print(df_отсортированный)

# Фильтруем данные
df_фильтрованный = фильтровать_по_диапазону(df, '1.0-1.5')
print("\nФильтрованный DataFrame (1.0-1.5):")
print(df_фильтрованный)

# Строим гистограмму
plt.figure(figsize=(8, 5))
df['диапазон'].value_counts().sort_index().plot(kind='bar')
plt.title('Распределение по соотношению сторон')
plt.xlabel('Диапазон соотношения')
plt.ylabel('Количество изображений')

# Сохраняем, потом показываем
plt.savefig('гистограмма.png')
plt.show()

# Сохраняем DataFrame
df.to_csv('данные.csv', index=False)

print("\nДанные сохранены в 'данные.csv'")
print("График сохранен в 'гистограмма.png'")