import argparse
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import sys
import os


def read_audio_file(file_path):
    """
    Чтение аудиофайла с помощью soundfile
    Возвращает частоту дискретизации и аудиоданные
    """
    try:
        data, samplerate = sf.read(file_path)
        return samplerate, data
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)


def print_audio_info(sample_rate, audio_data):
    """Отображение информации об аудиофайле"""
    duration = len(audio_data) / sample_rate
    print(f"Частота дискретизации: {sample_rate} Hz")
    print(f"Размер аудио: {len(audio_data)} сэмплов")
    print(f"Длительность: {duration:.2f} секунд")
    
    if len(audio_data.shape) == 1:
        print("Тип: Моно")
        print(f"Диапазон амплитуд: [{audio_data.min():.3f}, {audio_data.max():.3f}]")
    else:
        print("Тип: Стерео")
        print(f"Количество каналов: {audio_data.shape[1]}")
        print(f"Диапазон амплитуд левого канала: [{audio_data[:, 0].min():.3f}, {audio_data[:, 0].max():.3f}]")
        print(f"Диапазон амплитуд правого канала: [{audio_data[:, 1].min():.3f}, {audio_data[:, 1].max():.3f}]")
    
    return duration


def trim_audio(audio_data, sample_rate, start_time, end_time):
    """
    Обрезка аудио в указанном временном интервале
    start_time: время начала (секунды)
    end_time: время окончания (секунды)
    """
    start_sample = int(start_time * sample_rate)
    end_sample = int(end_time * sample_rate)
    
    start_sample = max(0, start_sample)
    end_sample = min(len(audio_data), end_sample)
    
    if start_sample >= end_sample:
        print("Ошибка: Время начала должно быть меньше времени окончания")
        sys.exit(1)
    
    if len(audio_data.shape) == 1:
        trimmed_audio = audio_data[start_sample:end_sample]
    else:
        trimmed_audio = audio_data[start_sample:end_sample, :]
    
    return trimmed_audio


def plot_audio_comparison(original_audio, trimmed_audio, sample_rate, original_duration, start_time, end_time):
    """Построение графика сравнения исходного и обрезанного аудио"""
    time_original = np.linspace(0, original_duration, len(original_audio))
    time_trimmed = np.linspace(start_time, end_time, len(trimmed_audio))
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    if len(original_audio.shape) == 1:
        ax1.plot(time_original, original_audio, 'b-', alpha=0.7, linewidth=0.5)
        ax1.set_ylabel('Амплитуда')
        ax1.set_title('Исходное аудио')
    else:
        ax1.plot(time_original, original_audio[:, 0], 'b-', alpha=0.7, linewidth=0.5, label='Левый канал')
        ax1.plot(time_original, original_audio[:, 1], 'r-', alpha=0.7, linewidth=0.5, label='Правый канал')
        ax1.legend()
        ax1.set_ylabel('Амплитуда')
        ax1.set_title('Исходное аудио (Стерео)')
    
    ax1.axvspan(start_time, end_time, color='red', alpha=0.3, label='Область обрезки')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    if len(trimmed_audio.shape) == 1:
        ax2.plot(time_trimmed, trimmed_audio, 'g-', alpha=0.7, linewidth=0.5)
        ax2.set_ylabel('Амплитуда')
        ax2.set_title('Обрезанное аудио')
    else:
        ax2.plot(time_trimmed, trimmed_audio[:, 0], 'b-', alpha=0.7, linewidth=0.5, label='Левый канал')
        ax2.plot(time_trimmed, trimmed_audio[:, 1], 'r-', alpha=0.7, linewidth=0.5, label='Правый канал')
        ax2.legend()
        ax2.set_ylabel('Амплитуда')
        ax2.set_title('Обрезанное аудио (Стерео)')
    
    ax2.set_xlabel('Время (секунды)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def save_audio_file(file_path, sample_rate, audio_data):
    """Сохранение аудиофайла с помощью soundfile"""
    try:
        sf.write(file_path, audio_data, sample_rate)
        print(f"Обрезанное аудио сохранено в: {file_path}")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Обрезка аудио в указанном временном интервале')
    parser.add_argument('input_file', help='Путь к входному аудиофайлу')
    parser.add_argument('output_file', help='Путь для сохранения выходного аудиофайла')
    parser.add_argument('start_time', type=float, help='Время начала обрезки (секунды)')
    parser.add_argument('end_time', type=float, help='Время окончания обрезки (секунды)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Ошибка: Входной файл '{args.input_file}' не существует")
        sys.exit(1)
    
    if args.start_time < 0 or args.end_time < 0:
        print("Ошибка: Время не может быть отрицательным")
        sys.exit(1)
    
    if args.start_time >= args.end_time:
        print("Ошибка: Время начала должно быть меньше времени окончания")
        sys.exit(1)
    
    print("Чтение аудиофайла...")
    sample_rate, original_audio = read_audio_file(args.input_file)
    
    print("\n=== ИНФОРМАЦИЯ ОБ ИСХОДНОМ АУДИО ===")
    original_duration = print_audio_info(sample_rate, original_audio)
    
    if args.end_time > original_duration:
        print(f"Предупреждение: Время окончания ({args.end_time}s) превышает длительность аудио ({original_duration:.2f}s)")
        args.end_time = original_duration
    
    print(f"\nОбрезка аудио с {args.start_time}s по {args.end_time}s...")
    trimmed_audio = trim_audio(original_audio, sample_rate, args.start_time, args.end_time)
    
    print("\n=== ИНФОРМАЦИЯ ОБ ОБРЕЗАННОМ АУДИО ===")
    trimmed_duration = len(trimmed_audio) / sample_rate
    print_audio_info(sample_rate, trimmed_audio)
    
    print("\nОтображение графика сравнения...")
    plot_audio_comparison(original_audio, trimmed_audio, sample_rate, original_duration, args.start_time, args.end_time)
    
    print("\nСохранение обрезанного аудио...")
    save_audio_file(args.output_file, sample_rate, trimmed_audio)
    
    print(f"\nЗавершено! Аудио успешно обрезано и сохранено.")
    print(f"Новая длительность: {trimmed_duration:.2f} секунд")

if __name__ == "__main__":
    main()