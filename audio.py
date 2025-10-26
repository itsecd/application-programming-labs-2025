import csv
import os
import random
import re
import requests

from bs4 import BeautifulSoup


class AudioIterator:
    def __init__(self, source):
        self.paths = []

        if isinstance(source, str):
            if source.endswith(".csv"):
                with open(source, "r", encoding="utf-8") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        self.paths.append(row["Absolute Path"])
            else:
                for file in os.listdir(source):
                    if file.endswith((".mp3", ".wav", ".ogg")):
                        self.paths.append(os.path.join(source, file))

        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        raise StopIteration


class AudioParser:

    def __init__(self, download_dir, annotation_file):
        self.url = "https://mixkit.co/free-stock-music"
        self.download_dir = download_dir
        self.annotation_file = annotation_file

    def create_annotation(self) -> None:
        """Write annotation csv file"""
        with open(self.annotation_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Absolute Path", "Relative Path"])

            for filename in os.listdir(self.download_dir):
                abs_path = os.path.abspath(os.path.join(self.download_dir, filename))
                rel_path = os.path.join(self.download_dir, filename)
                writer.writerow([abs_path, rel_path])

    def get_mood_list(self) -> list[str]:
        """Parse html to get mood links as list"""

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(self.url, headers=headers)
        if not response.ok:
            raise ConnectionError(f"Can't connect to {self.url}")
        html = response.text

        soup = BeautifulSoup(html, "html.parser")

        links = soup.find_all(
            "a",
            attrs={
                "class": "global-navigation__link",
                "href": re.compile(r"/free-stock-music/mood/*"),
            },
        )
        mood_links = []
        for link in links:
            mood_links.append((link["href"]))
        return mood_links

    def download_audios(self, count: int) -> None:
        os.makedirs(self.download_dir, exist_ok=True)
        downloaded_count = 0

        while downloaded_count < count:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            mood_links = self.get_mood_list()
            mood = mood_links[random.randint(0, len(mood_links))]
            target_url = "https://mixkit.co" + mood
            response = requests.get(target_url, headers=headers)
            if not response.ok:
                raise ConnectionError(f"Can't connect to {target_url}")
            html = response.text

            soup = BeautifulSoup(html, "html.parser")

            audios = soup.find_all(
                "div",
                attrs={
                    "data-test-id": "audio-player",
                    "data-controller": "audio-player",
                },
            )
            names = soup.find_all("h2", {"class": "item-grid-card__title"})
            for audio in audios:
                filename = (
                    os.path.basename(mood)
                    + "-"
                    + names[downloaded_count].get_text(strip=True)
                    + "-"
                    + os.path.basename(audio["data-audio-player-preview-url-value"])
                )
                filepath = os.path.join(self.download_dir, filename)

                with open(filepath, "wb") as f:
                    f.write(
                        requests.get(
                            audio["data-audio-player-preview-url-value"]
                        ).content
                    )

                downloaded_count += 1
                print(f"Downloaded {downloaded_count}/{count}: {filename}")
