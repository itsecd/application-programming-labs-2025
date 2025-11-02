import numpy
import argparse
import soundfile as sf
import matplotlib.pyplot as plt
import os





def load_music(path:str) ->  np.ndarray:
    data, samplerate = sf.read(filepath)
    return data

def create_echo(audio_data: np.ndarray, delay_samples: int, decay: float) -> np.ndarray:
    output_size = len(audio_data) + delay_samples
    result = np.zeros(output_size, dtype=audio_data.dtype)
    
    result[:len(audio_data)] = audio_data
    
    result[delay_samples:delay_samples + len(audio_data)] += audio_data * decay
    
    return result

def save_audio(audio_data: np.ndarray, filepath: str, samplerate: int = 44100) -> None:
     sf.write(filepath, audio_data, samplerate)
     
def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.
    
    Returns:
        argparse.Namespace: объект с аргументами
    """
    
    parser = argparse.ArgumentParser(
        description='Применяет эхо-эффект к аудиофайлу'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='Путь к исходному аудиофайлу'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Путь для сохранения результата'
    )
   
    
    return parser.parse_args()

def visualize(original: np.ndarray, echo: np.ndarray, delay_samples: int, samplerate: int = 44100) -> None:
    """
    Визуализирует исходный и обработанный сигналы.
    
    Args:
        original (np.ndarray): исходный массив сэмплов
        echo (np.ndarray): массив с эхо-эффектом
        delay_samples (int): Задержка в сэмплах
        samplerate (int): Частота дискретизации (default: 44100)
        
    Returns:
        None
    """
    
    samples_to_show = min(samplerate * 2, len(original))
    time_axis = np.arange(samples_to_show) / samplerate
    
    plt.figure(figsize=(14, 8))
    
    plt.subplot(2, 1, 1)
    plt.plot(time_axis, original[:samples_to_show], color='blue', linewidth=0.5)
    plt.title('Исходный сигнал', fontsize=12, fontweight='bold')
    plt.xlabel('Время (сек)')
    plt.ylabel('Амплитуда')
    plt.grid(True, alpha=0.3)
    plt.ylim(-1.1, 1.1)
    
    plt.subplot(2, 1, 2)
    echo_to_show = min(samples_to_show, len(echo))
    plt.plot(time_axis[:echo_to_show], echo[:echo_to_show], color='green', linewidth=0.5)
    plt.title('Сигнал с эхо-эффектом', fontsize=12, fontweight='bold')
    plt.xlabel('Время (сек)')
    plt.ylabel('Амплитуда')
    plt.grid(True, alpha=0.3)
    plt.ylim(-1.1, 1.1)
    
    delay_seconds = delay_samples / samplerate
    plt.figtext(0.5, 0.02, f'Задержка: {delay_seconds:.3f} сек ({delay_samples} сэмплов)',
                ha='center', fontsize=10)
    
    plt.tight_layout()
    plt.show()


def main() -> int:
    """
    Главная функция программы.
    
    Returns:
        int: код выхода (0 - успех, 1 - ошибка)
    """
    
    # Фиксированные параметры эхо
    DELAY = 0.3  # секунды
    DECAY = 0.6  # коэффициент затухания
    
    args = parse_arguments()
    
    try:
        if args.samplerate <= 0:
            raise ValueError("Частота дискретизации должна быть положительной")
        
        print("\n--- Загрузка файла ---")
        audio_data = load_audio(args.input)
        print(f"✓ Файл загружен: {args.input}")
        print(f"  Размер: {audio_data.shape}")
        
        print("\n--- Создание эхо-эффекта ---")
        delay_samples = int(DELAY * args.samplerate)
        echo_data = create_echo(audio_data, delay_samples, DECAY)
        print(f"✓ Эхо-эффект создан")
        print(f"  Задержка: {DELAY} сек ({delay_samples} сэмплов)")
        print(f"  Затухание: {DECAY}")
        print(f"  Новый размер: {echo_data.shape}")
        
        print("\n--- Визуализация ---")
        visualize(audio_data, echo_data, delay_samples, args.samplerate)
        
        print("\n--- Сохранение результата ---")
        save_audio(echo_data, args.output, args.samplerate)
        print(f"✓ Файл сохранён: {args.output}")
        
        print("\n✓ Готово!")
        return 0
        
    except FileNotFoundError as e:
        print(f"\n✗ Ошибка: {e}")
        return 1
    except ValueError as e:
        print(f"\n✗ Ошибка: {e}")
        return 1
    except RuntimeError as e:
        print(f"\n✗ Ошибка: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Неожиданная ошибка: {e}")
        return 1


if __name__ == '__main__':
    exit(main())