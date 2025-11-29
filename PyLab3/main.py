import argparse
import os

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import soundfile as sf


def read_audio(file_path):
    """Чтение аудиофайла и возврат частоты дискретизации и данных."""
    try:
        sample_rate, audio_data = wavfile.read(file_path)
        return sample_rate, audio_data
    except Exception:
        audio_data, sample_rate = sf.read(file_path)
        return sample_rate, audio_data


def get_audio_info(audio_data, sample_rate):
    """Получение информации об аудиофайле."""
    if len(audio_data.shape) == 1:
        channels = 1
        samples = len(audio_data)
    else:
        channels = audio_data.shape[1]
        samples = audio_data.shape[0]
    
    duration = samples / sample_rate
    data_type = audio_data.dtype
    
    return channels, samples, duration, data_type


def reduce_amplitude(audio_data, reduction_factor):
    """Уменьшение амплитуды сэмплов на заданную величину."""
    if audio_data.dtype == np.int16:
        audio_data_float = audio_data.astype(np.float32) / 32768.0
        reduced_audio = audio_data_float * reduction_factor
        reduced_audio = (reduced_audio * 32768.0).astype(np.int16)
    elif audio_data.dtype == np.int32:
        audio_data_float = audio_data.astype(np.float32) / 2147483648.0
        reduced_audio = audio_data_float * reduction_factor
        reduced_audio = (reduced_audio * 2147483648.0).astype(np.int32)
    else:
        reduced_audio = audio_data * reduction_factor
    
    return reduced_audio


def plot_audio_comparison(
    original_audio, 
    processed_audio, 
    sample_rate, 
    output_path
):
    """Создание графиков сравнения исходного и обработанного аудио."""
    max_samples = min(len(original_audio), 3 * sample_rate)
    time_axis = np.arange(max_samples) / sample_rate
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    def _plot_audio_signal(ax, audio, title, colors=('b-', 'r-'), alpha=0.7, linewidth=0.5):
        """Вспомогательная функция для построения аудиосигнала."""
        if len(audio.shape) == 1:
            ax.plot(time_axis, audio[:max_samples], colors[0], alpha=alpha, linewidth=linewidth)
        else:
            ax.plot(time_axis, audio[:max_samples, 0], colors[0], alpha=alpha, 
                   linewidth=linewidth, label='Канал 1')
            if audio.shape[1] > 1:
                ax.plot(time_axis, audio[:max_samples, 1], colors[1], alpha=alpha, 
                       linewidth=linewidth, label='Канал 2')
                ax.legend()
        
        ax.set_ylabel('Амплитуда')
        ax.set_xlabel('Время (секунды)')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
    
    # Построение исходного и обработанного аудио
    _plot_audio_signal(ax1, original_audio, 'Исходный аудиосигнал', ('b-', 'r-'))
    _plot_audio_signal(ax2, processed_audio, 'Обработанный аудиосигнал (уменьшенная амплитуда)', 
                      ('g-', 'm-'))
    
    plt.tight_layout()
    
    plot_filename = os.path.splitext(output_path)[0] + '_comparison.png'
    plt.savefig(plot_filename, dpi=150, bbox_inches='tight')
    print(f"График сравнения сохранен как: {plot_filename}")
    
    plt.show()

def main():
    """Основная функция программы."""
    parser = argparse.ArgumentParser(
        description='Обработка аудио: уменьшение амплитуды сэмплов'
    )
    parser.add_argument(
        '--input', 
        required=True, 
        help='Название входного аудиофайла'
    )
    parser.add_argument(
        '--output', 
        required=True, 
        help='Название выходного аудиофайла'
    )
    parser.add_argument(
        '--factor',
        type=float,
        default=0.5,
        help='Коэффициент уменьшения амплитуды (по умолчанию: 0.5)'
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Ошибка: Входной файл {args.input} не найден")
        exit(1)
    
    if args.factor <= 0 or args.factor > 1:
        print("Ошибка: Коэффициент уменьшения должен быть между 0 и 1")
        exit(1)
    
    print(f"Обработка аудиофайла: {args.input}")
    print(f"Коэффициент уменьшения амплитуды: {args.factor}")
    
    try:
        sample_rate, audio_data = read_audio(args.input)
        
        channels, samples, duration, data_type = get_audio_info(
            audio_data, 
            sample_rate
        )
        
        print("\nИнформация об аудиофайле:")
        print(f"  Частота дискретизации: {sample_rate} Гц")
        print(f"  Количество каналов: {channels}")
        print(f"  Количество сэмплов: {samples}")
        print(f"  Длительность: {duration:.2f} секунд")
        print(f"  Тип данных: {data_type}")
        
        processed_audio = reduce_amplitude(audio_data, args.factor)
        
        plot_audio_comparison(
            audio_data, 
            processed_audio, 
            sample_rate, 
            args.output
        )
        
        save_audio(processed_audio, sample_rate, args.output)
        
        print(f"\nОбработанный аудиофайл сохранен как: {args.output}")
        
    except Exception as e:
        print(f"Ошибка при обработке аудио: {e}")
        exit(1)


if __name__ == "__main__":
    main()