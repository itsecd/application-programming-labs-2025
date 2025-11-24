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
    
    if len(original_audio.shape) == 1:
        ax1.plot(
            time_axis, 
            original_audio[:max_samples], 
            'b-', 
            alpha=0.7, 
            linewidth=0.5
        )
        ax1.set_ylabel('Амплитуда')
    else:
        ax1.plot(
            time_axis,
            original_audio[:max_samples, 0],
            'b-',
            alpha=0.7,
            linewidth=0.5,
            label='Канал 1'
        )
        if original_audio.shape[1] > 1:
            ax1.plot(
                time_axis,
                original_audio[:max_samples, 1],
                'r-',
                alpha=0.7,
                linewidth=0.5,
                label='Канал 2'
            )
        ax1.set_ylabel('Амплитуда')
        ax1.legend()
    
    ax1.set_title('Исходный аудиосигнал')
    ax1.set_xlabel('Время (секунды)')
    ax1.grid(True, alpha=0.3)
    
    if len(processed_audio.shape) == 1:
        ax2.plot(
            time_axis,
            processed_audio[:max_samples],
            'g-',
            alpha=0.7,
            linewidth=0.5
        )
        ax2.set_ylabel('Амплитуда')
    else:
        ax2.plot(
            time_axis,
            processed_audio[:max_samples, 0],
            'g-',
            alpha=0.7,
            linewidth=0.5,
            label='Канал 1'
        )
        if processed_audio.shape[1] > 1:
            ax2.plot(
                time_axis,
                processed_audio[:max_samples, 1],
                'm-',
                alpha=0.7,
                linewidth=0.5,
                label='Канал 2'
            )
        ax2.set_ylabel('Амплитуда')
        ax2.legend()
    
    ax2.set_title('Обработанный аудиосигнал (уменьшенная амплитуда)')
    ax2.set_xlabel('Время (секунды)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    plot_filename = os.path.splitext(output_path)[0] + '_comparison.png'
    plt.savefig(plot_filename, dpi=150, bbox_inches='tight')
    print(f"График сравнения сохранен как: {plot_filename}")
    
    plt.show()


def save_audio(audio_data, sample_rate, output_path):
    """Сохранение аудиоданных в файл."""
    try:
        if audio_data.dtype in [np.int16, np.int32]:
            wavfile.write(output_path, sample_rate, audio_data)
        else:
            audio_data_int16 = (audio_data * 32768.0).astype(np.int16)
            wavfile.write(output_path, sample_rate, audio_data_int16)
    except Exception:
        sf.write(output_path, audio_data, sample_rate)


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