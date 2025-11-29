import numpy as np
import soundfile as sf

class AudioMixer:
    """Класс для работы со смешением аудиофайлов"""
    
    def read_audio_file(self, file_path)-> tuple[np.ndarray, int]:
        """Чтение аудиофайла и возврат данных и частоты дискретизации"""
        try:
            data, samplerate = sf.read(file_path)
            print(f"Загружен файл: {file_path}")
            print(f"Размер массива: {data.shape}")
            print(f"Частота дискретизации: {samplerate} Hz")
            print(f"Длительность: {len(data)/samplerate:.2f} секунд")
            return data, samplerate
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}: {e}")
            return None, None

    def mix_audio(self, audio1, audio2)-> np.ndarray:
        """
        Смешивает два аудиосигнала  усреднением

        """
        min_length = min(len(audio1), len(audio2))
        audio1 = audio1[:min_length]
        audio2 = audio2[:min_length]
    
        mixed_audio = (audio1 + audio2) / 2
        

        max_val = np.max(np.abs(mixed_audio))
        if max_val > 1.0:
            mixed_audio = mixed_audio / max_val
            print(f"Применена нормализация: пиковое значение {max_val:.3f}")
        
        return mixed_audio

    def mix_audio_files(self, file1, file2, output_path=None) -> tuple[bool, dict[str, np.ndarray | int]]:
        """
        Основной метод для смешения двух аудиофайлов
        """
        audio1, samplerate1 = self.read_audio_file(file1)
        audio2, samplerate2 = self.read_audio_file(file2)
        
        if audio1 is None or audio2 is None:
            return False, None
        
        if samplerate1 != samplerate2:
            print(f"Предупреждение: разные частоты дискретизации ({samplerate1} Hz и {samplerate2} Hz)")
            print("Будет использована частота первого файла")
        
        if len(audio1.shape) != len(audio2.shape):
            print("Предупреждение: разные форматы аудио (моно/стерео)")
            if len(audio1.shape) == 2:
                audio1 = np.mean(audio1, axis=1)
            if len(audio2.shape) == 2:
                audio2 = np.mean(audio2, axis=1)
        

        print("\nСмешивание аудио...")
        mixed_audio = self.mix_audio(audio1, audio2)
        
        print(f"Размер смешанного аудио: {mixed_audio.shape}")
        print(f"Длительность смешанного аудио: {len(mixed_audio)/samplerate1:.2f} секунд")
        
        if output_path:
            try:
                sf.write(output_path, mixed_audio, samplerate1)
                print(f"Смешанный аудиофайл сохранен как: {output_path}")
            except Exception as e:
                print(f"Ошибка при сохранении файла: {e}")
                return False, None
        
        result = {
            'audio1': audio1,
            'audio2': audio2,
            'mixed_audio': mixed_audio,
            'samplerate': samplerate1
        }
        
        return True, result