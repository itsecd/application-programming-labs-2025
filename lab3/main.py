import argparse
from audio_mixer import AudioMixer
from visual import AudioVisualizer

def get_args()-> argparse.Namespace:
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description='Смешение двух аудиофайлов')
    parser.add_argument('--input1', type=str, required=True, 
                       help='Путь к первому аудиофайлу')
    parser.add_argument('--input2', type=str, required=True,
                       help='Путь ко второму аудиофайлу')
    parser.add_argument('--output', type=str, default='mixed_audio.wav',
                       help='Путь для сохранения результата')
    return parser.parse_args()

def main()-> None:
    """Основная функция программы"""
    args = get_args()
    
    print(f"Аудиофайл 1: {args.input1}")
    print(f"Аудиофайл 2: {args.input2}")
    print(f"Выходной файл: {args.output}")
    print()
    
    mixer = AudioMixer()
    
    success, result = mixer.mix_audio_files(
        args.input1, 
        args.input2, 
        args.output
    )
    
    if not success:
        print("Ошибка при смешении аудиофайлов")
        return
    
    visualizer = AudioVisualizer()
    visualizer.create_comparison_plot(
        result['audio1'],
        result['audio2'], 
        result['mixed_audio'],
        result['samplerate'],
        args.output
    )
    
if __name__ == "__main__":
    main()