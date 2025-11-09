import os
import re
import csv
import time
import random
import requests
from typing import List, Dict
from config import HEADERS


def good_filename(name: str) -> str:
    name = re.sub(r'[^a-zA-Z0-9а-яА-ЯёЁ_.-]+', "_", name)
    name = re.sub(r'_+', "_", name)
    name = name.strip("_")
    
    if len(name) < 3:
        name = "nature_sound"
    
    return name[:80]


def download_sounds(sounds: List[Dict[str, str]],
                    dest_dir: str,
                    csv_path: str) -> int:
    os.makedirs(dest_dir, exist_ok=True)
    downloaded_count = 0

    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=[
                                "title", "absolute_path", "relative_path"])
        writer.writeheader()

        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.headers.update(HEADERS)

        for i, sound in enumerate(sounds, start=1):
            safe_name = good_filename(sound["title"])
            filename = f"{i:03d}_{safe_name}.mp3"
            file_path = os.path.join(dest_dir, filename)

            print(f"Downloading [{i}/{len(sounds)}]: {safe_name}")

            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                if file_size > 5000:
                    print(f"File already exists, skipping")
                    
                    abs_path = os.path.abspath(file_path)
                    rel_path = os.path.relpath(
                        file_path, start=os.path.dirname(csv_path))

                    writer.writerow({
                        "title": sound["title"],
                        "absolute_path": abs_path,
                        "relative_path": rel_path
                    })
                    
                    downloaded_count += 1
                    continue

            max_attempts = 2
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f"Attempt {attempt}/{max_attempts}...")
                    
                    time.sleep(random.uniform(0.5, 2.0))
                    
                    mp3_link = sound["mp3_link"]
                    
                    if "-preview" in mp3_link:
                        alt_link_1 = mp3_link.replace("-preview", "")
                        alt_link_2 = mp3_link.replace("/preview/", "/sfx/").replace("-preview", "")
                        
                        for alt_link in [alt_link_1, alt_link_2, mp3_link]:
                            try:
                                print(f"Trying URL: {alt_link.split('/')[-1]}")
                                resp = session.get(
                                    alt_link, 
                                    timeout=10,
                                    stream=True
                                )
                                
                                if resp.status_code == 200:
                                    mp3_link = alt_link
                                    break
                                else:
                                    resp.raise_for_status()
                            except:
                                continue
                    
                    resp = session.get(
                        mp3_link, 
                        timeout=10,
                        stream=True
                    )
                    resp.raise_for_status()

                    total_size = 0
                    
                    with open(file_path, "wb") as f:
                        for chunk in resp.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                total_size += len(chunk)
                    
                    if total_size < 3000:
                        print(f"Skipping (file too small: {total_size} bytes)")
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        break
                    
                    abs_path = os.path.abspath(file_path)
                    rel_path = os.path.relpath(
                        file_path, start=os.path.dirname(csv_path))

                    writer.writerow({
                        "title": sound["title"],
                        "absolute_path": abs_path,
                        "relative_path": rel_path
                    })
                    
                    downloaded_count += 1
                    print(f"Successfully downloaded: {filename} ({total_size} bytes)")
                    break

                except requests.exceptions.Timeout:
                    print(f"Timeout (attempt {attempt}/{max_attempts})")
                    if attempt == max_attempts:
                        print(f"Failed after {max_attempts} attempts")
                except requests.exceptions.RequestException as e:
                    print(f"Network error (attempt {attempt}/{max_attempts}): {e}")
                    if attempt == max_attempts:
                        print(f"Failed after {max_attempts} attempts")
                except Exception as e:
                    print(f"Unknown error (attempt {attempt}/{max_attempts}): {e}")
                    if attempt == max_attempts:
                        print(f"Failed after {max_attempts} attempts")
                
                if attempt < max_attempts:
                    time.sleep(1)

        session.close()

    return downloaded_count