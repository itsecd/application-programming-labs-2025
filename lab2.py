import csv
import os
import requests
import random
from bs4 import BeautifulSoup

class AudioIterator:
    def __init__(self, csv_file):
        self.data = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                self.data.append(row[0])
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.data):
            path = self.data[self.index]
            self.index += 1
            return path
        raise StopIteration

def download_audio(save_dir, annotation_file, count=50):
    
    instruments = ['flute', 'violin', 'drums']
    counts = [1, 1, 1]
    for i in range(count - 3):
        counts[random.randint(0, 2)] += 1
    
    print(f"Скачаем: флейта={counts[0]}, скрипка={counts[1]}, барабаны={counts[2]}")
    

    os.makedirs(save_dir, exist_ok=True)
    
    annotation = []
    downloaded = 0
    
    for instrument, need_count in zip(instruments, counts):
        print(f"Ищем {instrument}...")
        

        url = f"https://mixkit.co/free-stock-music/instrument/{instrument}/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            

            tracks = soup.find_all("div", class_="item-grid-card")
            
            for track in tracks[:need_count]:

                audio_div = track.find("div", attrs={"data-audio-player-preview-url-value": True})
                if audio_div:
                    audio_url = audio_div.get("data-audio-player-preview-url-value")
                    if audio_url:
 
                        filename = f"{instrument}_{downloaded+1}.mp3"
                        abs_path = os.path.abspath(os.path.join(save_dir, filename))
                        rel_path = os.path.join(save_dir, filename)
                        

                        audio_data = requests.get(audio_url)
                        with open(abs_path, 'wb') as f:
                            f.write(audio_data.content)
                        

                        annotation.append([abs_path, rel_path])
                        downloaded += 1
                        print(f"Скачано: {filename}")
                        
        except Exception as e:
            print(f"Ошибка с {instrument}: {e}")
            continue
    

    with open(annotation_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['absolute_path', 'relative_path'])
        writer.writerows(annotation)
    
    print(f"Готово! Скачано {downloaded} файлов")
    return downloaded

def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', required=True, help='Папка для файлов')
    parser.add_argument('--annotation', required=True, help='Файл аннотации')
    parser.add_argument('--count', type=int, default=50, help='Сколько скачать')
    args = parser.parse_args()
    

    download_audio(args.save_dir, args.annotation, args.count)
    

    print("\nПроверка итератора:")
    iterator = AudioIterator(args.annotation)
    for i, path in enumerate(iterator):
        print(f"{i+1}: {path}")
        if i >= 3:
            break

if __name__ == "__main__":
    main()