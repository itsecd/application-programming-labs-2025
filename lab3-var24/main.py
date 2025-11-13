import argparse
from audio_processor import load_audio, create_echo, save_audio
from visualization import visualize


def parse_arguments() -> argparse.Namespace:
    """Парсит аргументы командной строки"""

    parser = argparse.ArgumentParser(description="Применяет эхо-эффект к аудиофайлу")
    parser.add_argument("--input", help="Путь к исходному аудиофайлу")
    parser.add_argument("--output", help="Путь для сохранения результата")
    parser.add_argument("--delay", type=float, default=0.3, help="Задержка эхо в секундах")
    parser.add_argument("--decay", type=float, default=0.6, help="Коэффициент затухания")
    return parser.parse_args()


def main() -> int:
    """Главная функция программы"""

    args = parse_arguments()

    try:
        audio_data, samplerate = load_audio(args.input)
        
        delay_samples = int(args.delay * samplerate)
        echo_data = create_echo(audio_data, delay_samples, args.decay)

        visualize(audio_data, echo_data, delay_samples, samplerate)

        save_audio(echo_data, args.output, samplerate)

    except Exception as e:
        print(f"Ошибка при выполнении программы: {e}")
        

if __name__ == "__main__":
    main()