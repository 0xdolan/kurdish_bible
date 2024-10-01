#!/usr/bin/env python

import json
from pathlib import Path
from urllib.parse import unquote

import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore

CURRENT_DIR = Path(__file__).resolve().parent

# Directory to save JSON files
output_dir = Path("output_files")
output_dir.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist

# Directory to save audio files
audio_dir = Path("audio_files")
audio_dir.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist

# URL = "https://www.horami.org/en/genesis"
# AUDIO = "https://media.ipsapps.org/hac/hac-audio/GEN_001.mp3"
# MAIN_URL = "https://media.ipsapps.org/hac/osa/bible/genesis/01-GEN-001.html"
# https://media.ipsapps.org/hac/osa/bible/genesis/01-GEN-001.html
# https://media.ipsapps.org/hac/osa/bible/exodus/02-EXO-001.html
# https://media.ipsapps.org/hac/osa/bible/ruth/08-RUT-001.html
# https://media.ipsapps.org/hac/osa/bible/john/43-JHN-001.html
# https://media.ipsapps.org/hac/osa/bible/jonah/32-JON-001.html


bible_books = {
    "Genesis": {"chapters": 50, "book_number": "01", "book_abbv": "GEN"},
    "Exodus": {"chapters": 40, "book_number": "02", "book_abbv": "EXO"},
    "Ruth": {"chapters": 4, "book_number": "08", "book_abbv": "RUT"},
    "Jonah": {"chapters": 4, "book_number": "32", "book_abbv": "JON"},
    "John": {"chapters": 21, "book_number": "43", "book_abbv": "JHN"},
}

# Iterate over the books
for book_name, book_info in bible_books.items():
    chapters = book_info.get("chapters", 0)
    book_number = book_info.get("book_number", "")
    book_abbv = book_info.get("book_abbv", "")

    # Create a directory for each book to store its audio files
    book_audio_dir = Path(f"audio_files/{book_name}")
    book_audio_dir.mkdir(
        parents=True, exist_ok=True
    )  # Create the directory if it doesn't exist

    # Collect all chapters for this book
    book_data = {"book": book_name, "book_number": book_number, "chapters": []}

    for ch in range(1, chapters + 1):
        page = str(ch).zfill(3)
        url = f"https://media.ipsapps.org/hac/osa/bible/{book_name.lower()}/{book_number}-{book_abbv}-{page}.html"

        res = requests.get(url)
        res.encoding = "utf-8"

        if res.status_code == 200:
            soup = BeautifulSoup(res.content.decode("utf-8"), "lxml")
            content = soup.select_one("#content")

            # Get chapter number
            chapter = soup.find("div", "c-drop").text.strip()
            audio_link = soup.select_one("source").get("src")

            # Collect verses
            txs_class = content.find_all("div", "txs")
            chapter_data = {
                "chapter": int(chapter),
                "audio_link": audio_link,
                "verses": [],
            }

            for item in txs_class:
                if item:
                    verse = item.get("id").replace("T", "").strip()
                    text = unquote(item.text)

                    # Handle cases where verse is formatted oddly with non-breaking space
                    if "\xa0" in text:
                        text = text.split("\xa0")
                        verse = text[0].strip()
                        text = text[1].strip()

                    chapter_data["verses"].append(
                        {
                            "verse": int(verse),
                            "text": text.strip(),
                        }
                    )

            # Append chapter data to book
            book_data["chapters"].append(chapter_data)

            # Download audio file for this chapter
            audio_res = requests.get(audio_link)
            if audio_res.status_code == 200:
                # Construct a proper filename for the audio, using English numerals for chapter
                audio_filename = (
                    f"{book_name}_{ch}.mp3"  # ch is already in English numerals
                )
                audio_path = (
                    book_audio_dir / audio_filename
                )  # Save audio in the respective book's folder

                with open(audio_path, "wb") as audio_file:
                    audio_file.write(audio_res.content)

                print(
                    f"Downloaded audio: {audio_filename} for {book_name} chapter {ch}"
                )

    # Save book data to a JSON file
    output_file = output_dir / f"{book_name}.json"
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(book_data, f, ensure_ascii=False, indent=4)

    print(f"Saved {book_name}.json")
