import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def get_subdirectory(audio):
    if audio.startswith("bix"):
        return "bix"

    if audio.startswith("gg"):
        return "gg"

    if audio[0].isdigit() or audio[0] == "_":
        return "number"

    return audio[0]


def audio_generate(word: str) -> str:

    load_dotenv()
    API_KEY = os.getenv("DICTIONARY")
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={API_KEY}"

    try:
        response = requests.get(url)

        data = response.json()

        if not data:
            return ""

        audio = data[0]["hwi"]["prs"][0]["sound"]["audio"]

        subdir = get_subdirectory(audio)
        mp3_url = f"https://media.merriam-webster.com/audio/prons/en/us/mp3/{subdir}/{audio}.mp3"

        folder = Path("audios")
        folder.mkdir(exist_ok=True)

        filename = Path(urlparse(url).path).name + ".mp3"
        path = folder / filename

        response = requests.get(mp3_url, timeout=20)
        response.raise_for_status()

        path.write_bytes(response.content)

        return str(path)
    except Exception as e:
        print(f"Erro:{e}")

    return "None"
