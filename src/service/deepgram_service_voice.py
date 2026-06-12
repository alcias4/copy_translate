import os
import re
import time
from pathlib import Path

from deepgram import DeepgramClient
from dotenv import load_dotenv

load_dotenv()


def get_audio_models(text):
    api_key = os.getenv("DEEPGRAM_API_KEY")
    unique_value = int(time.time())

    client = DeepgramClient(api_key=api_key)
    audio_folder = Path("audios")
    data_folder = Path("dataVoice")

    audio_folder.mkdir(exist_ok=True)
    data_folder.mkdir(exist_ok=True)

    file_name = re.sub(r"[^a-zA-Z0-9_-]", "_", text)[:80] + f"{unique_value}.mp3"

    output_oficial = audio_folder / file_name
    output_data = data_folder / file_name

    response = client.speak.v1.audio.generate(
        text=text,
        model="aura-2-thalia-en",
    )

    with output_oficial.open("wb") as file1, output_data.open("wb") as file2:
        for chunk in response:
            file1.write(chunk)
            file2.write(chunk)

    return output_oficial
