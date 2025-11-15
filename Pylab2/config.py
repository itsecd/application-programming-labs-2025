"""Configuration settings for the Mixkit sound downloader."""

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/octet-stream;q=0.8,*/*;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "identity",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "audio",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
}

NATURE_SOUNDS_URL = "https://mixkit.co/free-sound-effects/nature/"