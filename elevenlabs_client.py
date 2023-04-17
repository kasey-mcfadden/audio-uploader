import requests
from dotenv import load_dotenv
from urllib.parse import quote
import requests
import os
from io import BytesIO
load_dotenv()

elevenLabsApiKey = os.environ.get('ELEVEN_LABS_API_KEY')
voice_id = "IHMMqNaUtMooU2Q3wLVK"

def text_to_speech(text: str) -> BytesIO:
    """
    This function sends a POST request to the Eleven Labs Text-to-Speech API
    to convert the given text to speech using the specified voice settings.
    The resulting audio file is saved as 'output.mp3' in the current directory.

    Returns:
        None
    """
    url = "https://api.elevenlabs.io/v1/text-to-speech/{}".format(voice_id)
    headers = {
        "accept": "audio/mpeg",
        "xi-api-key": elevenLabsApiKey,
        "Content-Type": "application/json",
    }
    data = {
        "text": text,
        "voice_settings": {"stability": 0, "similarity_boost": 0},
    }
    if not text or not text.strip():
        raise Exception('Error: cannot convert empty text to speech')
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        try:
            mp3 = BytesIO(response.content)
            print("Created mp3 content")
            return mp3
        except Exception as error:
            print("An error occurred creating audio:", error)
    else:
        print("Error:", response.status_code, response.text)
    
    return None

def main():
    """
    The main function of the program.
    """
    text = "Hello! Different test now. Listen to my voice."
    raw_mp3 = text_to_speech(text)
    with open("output.mp3", "wb") as f:
        f.write(raw_mp3)

if __name__ == '__main__':
    main()