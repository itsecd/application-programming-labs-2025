import time
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

from config import HEADERS


def fetch_page(url: str, timeout: int = 10) -> Optional[str]:
    """Fetch HTML content from a URL.
    
    Args:
        url: URL to fetch
        timeout: Request timeout in seconds
        
    Returns:
        Optional[str]: HTML content as string or None if failed
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"Error loading page {url}: {e}")
        return None


def extract_nature_sounds_from_html(html: str) -> List[Dict[str, str]]:
    """Extract sound information from HTML content.
    
    Args:
        html: HTML content to parse
        
    Returns:
        List[Dict[str, str]]: List of sound dictionaries with title and mp3_link
    """
    soup = BeautifulSoup(html, "html.parser")
    sounds = []

    sound_cards = soup.find_all('div', class_='item-grid-card')
    print(f"Found {len(sound_cards)} sound cards on page")

    for card in sound_cards:
        # Find audio player element
        audio_player = card.find('div', {'data-audio-player-preview-url-value': True})
        if not audio_player:
            continue
            
        mp3_link = audio_player.get('data-audio-player-preview-url-value')
        
        # Extract title from various possible elements
        title_element = card.find('h4', class_='item-grid-card__title')
        if title_element:
            title = title_element.get_text(strip=True)
        else:
            desc_element = card.find('p', class_='item-grid-card__description')
            if desc_element:
                title = desc_element.get_text(strip=True)
            else:
                url_part = mp3_link.split('/')[-1].replace('.mp3', '') if mp3_link else f"sound_{len(sounds)+1}"
                title = f"Nature_Sound_{url_part}"

        # Handle special case titles
        if "Unlimited creative assets" in title:
            if mp3_link:
                sound_id = mp3_link.split('/')[-1].replace('.mp3', '')
                title = f"Nature_Sound_{sound_id}"

        # Process valid MP3 links
        if mp3_link and mp3_link.startswith("http"):
            if "/preview/" in mp3_link:
                filename = mp3_link.split('/')[-1].replace("-preview", "")
                mp3_link = mp3_link.replace("/preview/", "/sfx/").replace(
                    mp3_link.split('/')[-1], filename
                )
            
            sounds.append({
                "title": title[:80],
                "mp3_link": mp3_link,
            })
            print(f"Found sound: {title} -> {mp3_link.split('/')[-1]}")

    return sounds


def fetch_nature_sounds(url: str, num_sounds: int) -> List[Dict[str, str]]:
    """Fetch nature sounds from Mixkit category pages.
    
    Args:
        url: Base URL of the category
        num_sounds: Maximum number of sounds to fetch
        
    Returns:
        List[Dict[str, str]]: List of sound dictionaries
    """
    sounds = []
    page = 1
    max_pages = 3
    
    print("Starting page parsing...")

    while len(sounds) < num_sounds and page <= max_pages:
        # Construct page URL
        if page == 1:
            page_url = url
        else:
            page_url = f"{url}?page={page}"

        print(f"Loading page {page}: {page_url}")
        
        html = fetch_page(page_url)
        if not html:
            # Try alternative URL format
            if page > 1:
                page_url = f"{url}page/{page}/"
                print(f"Trying alternative URL: {page_url}")
                html = fetch_page(page_url)
            
            if not html:
                print(f"Failed to load page {page}, stopping parsing")
                break

        # Extract sounds from current page
        page_sounds = extract_nature_sounds_from_html(html)
        if not page_sounds:
            print(f"No sounds found on page {page}, stopping parsing")
            break

        # Filter out duplicates
        existing_links = {s["mp3_link"] for s in sounds}
        new_sounds = [s for s in page_sounds if s["mp3_link"] not in existing_links]
        
        sounds.extend(new_sounds)
        print(f"Page {page} processed, new sounds: {len(new_sounds)}, total: {len(sounds)}")

        # Check if we've reached the desired number
        if len(sounds) >= num_sounds:
            print(f"Reached limit of {num_sounds} sounds")
            break

        page += 1
        time.sleep(1)

    return sounds[:num_sounds]