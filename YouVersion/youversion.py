#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Data From: https://www.bible.com/

import json
from pathlib import Path

import requests  # type: ignore
from rich.progress import track

current_directory = Path(__file__).resolve().parent


def get_bible_data(language):

    MAIN_URL = (
        f"https://www.bible.com/_next/data/nogh7EKJmNa2jhmizj0rV/en/audio-bible/503/"
    )
    BOOKS = [
        "GEN",
        "EXO",
        "LEV",
        "NUM",
        "DEU",
        "JOS",
        "JDG",
        "RUT",
        "1SA",
        "2SA",
        "1KI",
        "2KI",
        "1CH",
        "2CH",
        "EZR",
        "NEH",
        "EST",
        "JOB",
        "PSA",
        "PRO",
        "ECC",
        "SNG",
        "ISA",
        "JER",
        "LAM",
        "EZK",
        "DAN",
        "HOS",
        "JOL",
        "AMO",
        "OBA",
        "JON",
        "MIC",
        "NAM",
        "HAB",
        "ZEP",
        "HAG",
        "ZEC",
        "MAL",
        "MAT",
        "MRK",
        "LUK",
        "JHN",
        "ACT",
        "ROM",
        "1CO",
        "2CO",
        "GAL",
        "EPH",
        "PHP",
        "COL",
        "1TH",
        "2TH",
        "1TI",
        "2TI",
        "TIT",
        "PHM",
        "HEB",
        "JAS",
        "1PE",
        "2PE",
        "1JN",
        "2JN",
        "3JN",
        "JUD",
        "REV",
    ]

    # Intro
    for chapter_index, book in track(enumerate(BOOKS, 1)):
        book_dir = current_directory / language / f"{chapter_index:02d}_{book}"
        book_dir.mkdir(parents=True, exist_ok=True)

        intro_url = f"{MAIN_URL}{book}.INTRO1.{language}.json?versionId=503&usfm={book}.INTRO1.{language}"
        intro_response = requests.get(intro_url)
        if intro_response.status_code == 200:
            intro_data = intro_response.json()
            with open(book_dir / "intro.json", "w", encoding="utf-8") as json_file:
                json.dump(intro_data, json_file, ensure_ascii=False)

        # Books
        for chapter_index in range(100):
            chapter_url = f"{MAIN_URL}{book}.{chapter_index}.{language}.json?versionId=503&usfm={book}.{chapter_index}.{language}"
            main_response = requests.get(chapter_url)
            if main_response.status_code == 200:
                main_data = main_response.json()
                with open(
                    book_dir / f"{chapter_index}.json", "w", encoding="utf-8"
                ) as json_file:
                    json.dump(main_data, json_file, ensure_ascii=False)


languages = {
    "KSS": "Kurdi Sorani Standard (كوردی سۆرانی ستانده‌رد)",
    "PNTZS": "the New Testaments and Psalms in Kurdish Sorani (پەیمانی نوێ و زەبوورەکان بە سۆرانی)",
    "BHD": "Kurdish Behdini 2019 Kurdish Literature Association (NT) Non Drama",
    "KURNT": "Kurmanji Încîl",
    "KMRNTL": "Peymana Nû (Încîl)",
    "MKRPRO": "Methelokên Hezretê Silêman 1947",
}

for language_abbv, language_fullname in languages.items():
    print()
    print(f"{language_fullname} is downloading ...")
    get_bible_data(language_abbv)
    print(f"{language_fullname} is finished ...\n")


print("Done!")
