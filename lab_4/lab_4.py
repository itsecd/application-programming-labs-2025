import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import librosa
import os
from pathlib import Path

# Создание DataFrame из CSV
df = pd.read_csv('annotation.csv')

# Переименование колонок для отражения содержимого
df = df.rename(columns={
    'absolute_path': 'Абсолютный_путь_к_файлу',
    'relative_path': 'Относительный_путь_к_файлу',
    'filename': 'Имя_файла',
    'duration_seconds': 'Длительность_секунды',
    'file_size_mb': 'Размер_файла_МБ'
})

# Функция для получения максимальной амплитуды аудиофайла
def get_max_amplitude(file_path):
    """
    Получает максимальную амплитуду аудиофайла по модулю
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            print(f"Файл не найден: {file_path}")
            return 0.0
        
        # Загружаем аудиофайл с помощью librosa
        audio_data, sample_rate = librosa.load(file_path, sr=None)
        
        # Находим максимальную амплитуду по модулю
        max_amplitude = np.max(np.abs(audio_data))
        
        return max_amplitude
        
    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")
        return 0.0

# Добавляем колонку с максимальной амплитудой
print("Добавление колонки с максимальной амплитудой...")
df['Максимальная_амплитуда'] = df['Абсолютный_путь_к_файлу'].apply(get_max_amplitude)

# Функция сортировки по максимальной амплитуде
def sort_by_amplitude(df, ascending=True):
    """
    Сортирует DataFrame по колонке максимальной амплитуды
    """
    return df.sort_values('Максимальная_амплитуда', ascending=ascending)

# Функция фильтрации по максимальной амплитуде
def filter_by_amplitude(df, min_amplitude=0.0, max_amplitude=1.0):
    """
    Фильтрует DataFrame по диапазону максимальной амплитуды
    """
    return df[(df['Максимальная_амплитуда'] >= min_amplitude) & 
              (df['Максимальная_амплитуда'] <= max_amplitude)]

# Применяем сортировку
df_sorted = sort_by_amplitude(df, ascending=False)
print("Данные отсортированы по максимальной амплитуде")

# Применяем фильтрацию (например, только файлы с амплитудой больше 0.1)
df_filtered = filter_by_amplitude(df, min_amplitude=0.1)
print(f"После фильтрации осталось {len(df_filtered)} файлов из {len(df)}")

# Создаем график
plt.figure(figsize=(12, 8))

# График для всех отсортированных данных
x_positions = range(len(df_sorted))
y_values = df_sorted['Максимальная_амплитуда'].values

plt.plot(x_positions, y_values, 'b-', linewidth=2, alpha=0.7, label='Максимальная амплитуда')
plt.scatter(x_positions, y_values, c=y_values, cmap='viridis', s=50, alpha=0.6)

# Настройки графика
plt.xlabel('Номер аудиофайла в отсортированном списке', fontsize=12)
plt.ylabel('Максимальная амплитуда', fontsize=12)
plt.title('Распределение максимальной амплитуды аудиофайлов', fontsize=14, fontweight='bold')
plt.colorbar(label='Максимальная амплитуда')
plt.grid(True, alpha=0.3)
plt.legend()

# Улучшаем читаемость
plt.tight_layout()

# Сохраняем график
plt.savefig('audio_amplitude_plot.png', dpi=300, bbox_inches='tight')
print("График сохранен как 'audio_amplitude_plot.png'")

# Показываем график
plt.show()

# Сохраняем DataFrame с новой колонкой
output_df = df_sorted[['Абсолютный_путь_к_файлу', 'Относительный_путь_к_файлу', 'Максимальная_амплитуда']]
output_df.to_csv('audio_data_with_amplitude.csv', index=False, encoding='utf-8')
print("DataFrame сохранен как 'audio_data_with_amplitude.csv'")

# Дополнительная информация
print("\n" + "="*50)
print("СТАТИСТИКА ПО АМПЛИТУДАМ:")
print(f"Всего файлов: {len(df)}")
print(f"Максимальная амплитуда: {df['Максимальная_амплитуда'].max():.4f}")
print(f"Минимальная амплитуда: {df['Максимальная_амплитуда'].min():.4f}")
print(f"Средняя амплитуда: {df['Максимальная_амплитуда'].mean():.4f}")
print(f"Медианная амплитуда: {df['Максимальная_амплитуда'].median():.4f}")

# Топ-5 файлов с наибольшей амплитудой
print("\nТОП-5 файлов с наибольшей амплитудой:")
top_5 = df_sorted.head()[['Имя_файла', 'Максимальная_амплитуда']]
for idx, row in top_5.iterrows():
    print(f"  {row['Имя_файла']}: {row['Максимальная_амплитуда']:.4f}")

# Дополнительный анализ: гистограмма распределения амплитуд
plt.figure(figsize=(10, 6))
plt.hist(df['Максимальная_амплитуда'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
plt.xlabel('Максимальная амплитуда')
plt.ylabel('Количество файлов')
plt.title('Распределение максимальных амплитуд аудиофайлов')
plt.grid(True, alpha=0.3)
plt.savefig('amplitude_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nДополнительная гистограмма сохранена как 'amplitude_distribution.png'")