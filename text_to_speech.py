# text_to_voice.py
from gtts import gTTS
import pygame
import time
import os
import tempfile

LANG_MAP = {"english": "en","hindi": "hi","marathi": "mr"
}
_selected_lang = "en"

def set_language(lang_key: str):
    global _selected_lang
    _selected_lang = LANG_MAP.get(lang_key, "en")

def _play_file(path):
 #Play an audio file using pygame and block until finished."""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        print("Audio playback error:", e)
    finally:
        try:
            pygame.mixer.quit()
        except Exception:
            pass

def speak(text: str, lang_key: str = None):

#Speak `text` using gTTS in the selected language (or override via lang_key).
#This saves a temporary mp3, plays it, then deletes it.

    lang_code = _selected_lang if lang_key is None else LANG_MAP.get(lang_key, _selected_lang)
    # Print as console fallback
    prefix = {"en": "Chatbot:", "hi": "बॉट:", "mr": "बॉट:"}.get(lang_code, "Chatbot:")
    print(f"{prefix} {text}")

    try:
        fd, tmp_path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)
        tts = gTTS(text=text, lang=lang_code)
        tts.save(tmp_path)
        _play_file(tmp_path)
    except Exception as e:
        print("TTS error:", e)
    finally:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass