import soundfile as sf

from func2 import (get_args, echo_effect, plot_audio, save_audio)


def main(input_path: str, output_path: str, delay: float, alpha: float) -> None:
    """Главная функция обработки аудио с эхо-эффектом.

    Args:
        input_path (str): Путь к исходному аудио.
        output_path (str): Путь для сохранения результата.
        delay (float): Задержка эхо (сек).
        alpha (float): Усиление эхо.
    """
    audio, sr = sf.read(input_path)
    print(f"Размер аудио: {audio.shape}, частота: {sr}")

    if audio.ndim != 1:
        audio = audio.mean(axis=1)

    processed = echo_effect(audio, sr, delay, alpha)

    plot_audio(audio, processed, sr)

    save_audio(output_path, processed, sr)


if __name__ == "__main__":
    args = get_args()
    try:
        main(args.input, args.output, args.delay, args.alpha)
    except ValueError as err:
        print(f'Недопустимое значение: "{err}"')
    except FileNotFoundError as err:
        print(f'Файл не найден: "{err.filename}"')
    except Exception as err:
        print(f"Непредвиденная ошибка: {err}")
