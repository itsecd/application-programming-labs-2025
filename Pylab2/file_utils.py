import csv
import os
import random
import re
import time
from typing import Dict, List

import requests

from config import HEADERS


def good_filename(name: str) -> str:
    """Convert a string to a valid filename.
    
    Args:
        name: Original filename string
        
    Returns:
        str: Sanitized filename safe for filesystem
    """
    # Replace invalid characters with underscores
    name = re.sub(r'[^a-zA-Z0-9а-яА-ЯёЁ_.-]+', "_", name)
    name = re.sub(r'_+', "_", name)
    name = name.strip("_")
    
    # Ensure minimum length
    if len(name) < 3:
        name = "nature_sound"
    
    return name[:80]


def _handle_existing_file(file_path: str, sound: Dict[str, str], 
                         csv_path: str, writer: csv.DictWriter) -> bool:
    """Handle case when file already exists and is valid.
    
    Args:
        file_path: Path to existing file
        sound: Sound dictionary with title
        csv_path: Path to CSV annotation file
        writer: CSV writer object
        
    Returns:
        bool: True if file was valid and processed, False otherwise
    """
    file_size = os.path.getsize(file_path)
    if file_size > 5000:
        print(f"File already exists, skipping")
        
        abs_path = os.path.abspath(file_path)
        rel_path = os.path.relpath(file_path, start=os.path.dirname(csv_path))

        writer.writerow({
            "title": sound["title"],
            "absolute_path": abs_path,
            "relative_path": rel_path
        })
        return True
    return False


def _try_alternative_links(mp3_link: str, session: requests.Session) -> str:
    """Try alternative download links for preview files.
    
    Args:
        mp3_link: Original MP3 link
        session: Requests session object
        
    Returns:
        str: Working MP3 link
    """
    if "-preview" in mp3_link:
        alt_link_1 = mp3_link.replace("-preview", "")
        alt_link_2 = mp3_link.replace("/preview/", "/sfx/").replace("-preview", "")
        
        for alt_link in [alt_link_1, alt_link_2, mp3_link]:
            try:
                print(f"Trying URL: {alt_link.split('/')[-1]}")
                resp = session.get(alt_link, timeout=10, stream=True)
                
                if resp.status_code == 200:
                    return alt_link
                else:
                    resp.raise_for_status()
            except Exception:
                continue
    return mp3_link


def _download_file(session: requests.Session, mp3_link: str, 
                  file_path: str) -> int:
    """Download a single file and return its size.
    
    Args:
        session: Requests session object
        mp3_link: URL to download from
        file_path: Local path to save file
        
    Returns:
        int: File size in bytes, or 0 if download failed
    """
    try:
        resp = session.get(mp3_link, timeout=10, stream=True)
        resp.raise_for_status()

        total_size = 0
        with open(file_path, "wb") as file:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    total_size += len(chunk)
        
        return total_size
    except Exception as e:
        print(f"Download error: {e}")
        return 0


def _attempt_download(sound: Dict[str, str], file_path: str, 
                     session: requests.Session, max_attempts: int = 2) -> bool:
    """Attempt to download a sound file with retries.
    
    Args:
        sound: Sound dictionary with title and mp3_link
        file_path: Local path to save file
        session: Requests session object
        max_attempts: Maximum number of download attempts
        
    Returns:
        bool: True if download was successful, False otherwise
    """
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"Attempt {attempt}/{max_attempts}...")
            
            time.sleep(random.uniform(0.5, 2.0))
            
            # Try alternative links for preview files
            mp3_link = _try_alternative_links(sound["mp3_link"], session)
            
            # Download the file
            total_size = _download_file(session, mp3_link, file_path)
            
            if total_size < 3000:
                print(f"Skipping (file too small: {total_size} bytes)")
                if os.path.exists(file_path):
                    os.remove(file_path)
                return False
            
            print(f"Successfully downloaded: {os.path.basename(file_path)} ({total_size} bytes)")
            return True

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
    
    return False


def _write_to_csv(file_path: str, sound: Dict[str, str], 
                 csv_path: str, writer: csv.DictWriter) -> None:
    """Write file information to CSV annotation.
    
    Args:
        file_path: Path to the audio file
        sound: Sound dictionary with title
        csv_path: Path to CSV annotation file
        writer: CSV writer object
    """
    abs_path = os.path.abspath(file_path)
    rel_path = os.path.relpath(file_path, start=os.path.dirname(csv_path))

    writer.writerow({
        "title": sound["title"],
        "absolute_path": abs_path,
        "relative_path": rel_path
    })


def _setup_http_session() -> requests.Session:
    """Configure and return HTTP session for downloading.
    
    Returns:
        requests.Session: Configured session object
    """
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.headers.update(HEADERS)
    return session


def _process_single_sound(sound: Dict[str, str], index: int, total_count: int,
                         dest_dir: str, csv_path: str, writer: csv.DictWriter,
                         session: requests.Session) -> bool:
    """Process a single sound file (download or skip if exists).
    
    Args:
        sound: Sound dictionary with title and mp3_link
        index: Sound index for filename
        total_count: Total number of sounds being processed
        dest_dir: Destination directory
        csv_path: Path to CSV annotation file
        writer: CSV writer object
        session: HTTP session object
        
    Returns:
        bool: True if file was processed successfully, False otherwise
    """
    safe_name = good_filename(sound["title"])
    filename = f"{index:03d}_{safe_name}.mp3"
    file_path = os.path.join(dest_dir, filename)

    print(f"Downloading [{index}/{total_count}]: {safe_name}")

    # Skip if file already exists and is valid
    if os.path.exists(file_path):
        if _handle_existing_file(file_path, sound, csv_path, writer):
            return True

    # Attempt to download file
    if _attempt_download(sound, file_path, session):
        _write_to_csv(file_path, sound, csv_path, writer)
        return True
    
    return False


def download_sounds(
    sounds: List[Dict[str, str]],
    dest_dir: str,
    csv_path: str
) -> int:
    """Download audio files and create CSV annotation.
    
    Args:
        sounds: List of sound dictionaries with title and mp3_link
        dest_dir: Destination directory for downloaded files
        csv_path: Path for output CSV annotation file
        
    Returns:
        int: Number of successfully downloaded files
    """
    os.makedirs(dest_dir, exist_ok=True)
    downloaded_count = 0
    total_sounds = len(sounds)

    # Setup CSV file for annotation
    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["title", "absolute_path", "relative_path"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Configure HTTP session for downloading
        session = _setup_http_session()

        try:
            # Download each sound
            for i, sound in enumerate(sounds, start=1):
                if _process_single_sound(sound, i, total_sounds, dest_dir, 
                                       csv_path, writer, session):
                    downloaded_count += 1
        finally:
            session.close()

    return downloaded_count