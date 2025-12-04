# Импортируем модули
from arg_parser import parse_arguments
from audio_processor import read_audio_file, reverse_audio, save_audio_file
from visualizer import plot_audio_comparison


def main():
    """Основная функция"""
    try:
        args = parse_arguments()

        print("=" * 50)
        print("Чтение аудиофайла...")
        
        try:
            audio_data, sample_rate, channels = read_audio_file(args.input_file)
        except Exception as e:
            raise Exception(f"Ошибка при чтении файла: {e}")
            
        print("\n" + "=" * 50)
        print("Переворачивание аудио задом наперед...")
        
        try:
            reversed_audio = reverse_audio(audio_data)
        except Exception as e:
            raise Exception(f"Ошибка при переворачивании аудио: {e}")

        print("\n" + "=" * 50)
        print("Визуализация результатов...")
        
        try:
            plot_audio_comparison(
                audio_data, reversed_audio, sample_rate, args.input_file, args.output_file
            )
        except ImportError as e:
            print(f"Ошибка импорта matplotlib: {e}")
            print("Продолжаем без визуализации...")
        except Exception as e:
            print(f"Ошибка при визуализации: {e}")
            print("Продолжаем без визуализации...")

        print("\n" + "=" * 50)
        print("Сохранение результата...")
        
        try:
            save_audio_file(reversed_audio, sample_rate, args.output_file)
        except Exception as e:
            raise Exception(f"Ошибка при сохранении файла: {e}")


        print("\n" + "=" * 50)
        print("Готово!")
        print(f"Оригинальный файл: {args.input_file}")
        print(f"Обработанный файл: {args.output_file}")

    except SystemExit:
        pass
    except Exception as e:
        raise Exception(f"Критическая ошибка: {e}")



if __name__ == "__main__":
    main()