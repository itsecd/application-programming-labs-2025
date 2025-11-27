from pathlib import Path
import requests
from bs4 import BeautifulSoup
import os
import csv


instruments = ['trumpet', 'ukulele', 'harp']

def url_audio(instrument: str) -> list:
    urls = []
    link1 = "https://mixkit.co/free-stock-music/instrument/"
    
    try:
        resp = requests.get(f"{link1}{instrument}/", timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"Ошибка запроса страницы для {instrument}: {e}")
        return

    soup = BeautifulSoup(resp.text, 'lxml')

    main = soup.find('main')
    if not main:
        print('Main block not found, aborting')
        return
    ordering = main.find('div', class_='item-grid__ordering')
    if not ordering:
        print('Ordering block not found, aborting')
        return
    wrapper = ordering.find('div', class_='item-grid__wrapper')
    if not wrapper:
        print('Wrapper block not found, aborting')
        return
    items_block = wrapper.find('div', class_='item-grid__items')
    if not items_block:
        print('Items block not found, aborting')
        return

    all_audio = items_block.find_all('div', class_='item-grid__item')

    for audio in all_audio:
        card = audio.find('div', class_='item-grid-card item-grid-card--show-meta')
        if not card:
            continue
        audio_player = card.find('div', {'data-test-id': 'audio-player'})
        if not audio_player:
            continue

        audio_link = audio_player.get('data-audio-player-preview-url-value')
        if not audio_link:
            continue
        audio_link = audio_link.strip()

        urls.append(audio_link)

    return urls

def dowload_audio(instrument: str, urls: list, count: int)->list:
    audio_number = 0
    data = []
    
    download_dir = os.path.join('Downloads', instrument)
    os.makedirs(download_dir, exist_ok=True)
    
    for i in range(count):
        try:
            dl_resp = requests.get(urls[i], timeout=20)
            dl_resp.raise_for_status()
            audio_byts = dl_resp.content
        except Exception as e:
            print(f"Ошибка при загрузке {urls[i]}: {e}")
            continue

        out_path = os.path.join(download_dir, f"{audio_number}.mp3")
        try:
            with open(out_path, 'wb') as file:
                file.write(audio_byts)
            print(f'Аудио {audio_number}.mp3 успешно скачано в {download_dir}!')
        except Exception as e:
            print(f'Ошибка записи файла {out_path}: {e}')
            continue
        abs_path = Path(out_path).resolve()
        rel_path= Path(os.path.relpath(abs_path, start=Path.cwd()))
        data.append([f'{audio_number}.mp3', str(abs_path), str(rel_path)])
        audio_number += 1
    print('Все аудио обработаны для', instrument)
    return data

max_audio = 0

for instrument in instruments:
    if max_audio == 0:
        max_audio = len(url_audio(instrument))
    else:
        max_audio=min(max_audio, len(url_audio(instrument)))
data = []
for instrument in instruments:
    data.append(dowload_audio(instrument, url_audio(instrument), max_audio))
 
with open('data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Filename', 'Absolute Path', 'Relative Path'])
    for line in data:
        writer.writerows(line) 
    
    print('CSV файл успешно создан: data.csv')