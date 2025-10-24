import requests

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

def main():
    url = "https://mixkit.co/free-stock-music/instrument/trumpet/"
    
    html = fetch_page(url)
    
    if html:
        print("✅OK")
        print("LEN HTML:", len(html))
        print(html[:500])
    else:
        print("⚠️ERROR")

if __name__ == "__main__":
    main()


