import requests
from bs4 import BeautifulSoup
from typing import List, Dict

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}

def fetch_page(url: str, timeout: int = 2) -> str | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status() 
        return resp.text
    except Exception:
        return None

def extract_tracks_from_html(html: str) -> List[Dict[str, str]]:
    """
    output:
        [
            {"title": "song name", "mp3_link": "https://..."},
            ...
        ]
    """
    soup = BeautifulSoup(html, "html.parser")

    # контейнер со всеми блоками песен на странице
    # div.item-grid__items > [div.item-grig__item, ...]
    container = soup.select_one("div.item-grid__items")
    if not container:
        return [] 

    tracks = []

    for item in container.select("div.item-grid__item"):

        title_tag = item.select_one("h2.item-grid-card__title")
        player_tag = item.select_one('div[data-test-id="audio-player"]')

        if title_tag and player_tag:
            
            tracks.append({
                "title": title_tag.get_text(strip=True),
                "mp3_link": player_tag.get("data-audio-player-preview-url-value"),
            })

    return tracks

def main():
    url = "https://mixkit.co/free-stock-music/instrument/acoustic-guitar/"
    
    html = fetch_page(url)
    
    if html:
        print("✅OK")
        print("LEN HTML:", len(html))
    else:
        print("⚠️ERROR")

    print(extract_tracks_from_html(html))

if __name__ == "__main__":
    main()


