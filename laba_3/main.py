import os
import sys
from config import logger
from cli import parser_t
from audio_processor import transformations
from visualizer import plot_audio

def main():
    try:
        source, output_plot, output_audio, alpha = parser_t()
        
        if alpha < 1:
            raise ValueError("alpha должен быть ≥ 1")
        
        size = os.path.getsize(source)
        logger.info(f"Размер файла: {size} байт")
        
        data, data_sped, t_orig, t_sped = transformations(source, output_audio, alpha)
        plot_audio(data, data_sped, t_orig, t_sped, alpha, output_plot)
        
    except Exception as e:
        logger.error(e)
        sys.exit(1)


if __name__ == '__main__':
    main()