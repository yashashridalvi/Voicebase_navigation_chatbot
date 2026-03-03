import speech_recognition as sr


# Map simple language code to Google STT language code
LANG_TO_GOOGLE = {
"en": "en-IN", # English (India) accent
"hi": "hi-IN",
"mr": "mr-IN"
}




def listen(lang: str = "en", timeout: int = 7, phrase_time_limit: int = 8):
#Listen and return recognized text or None.

    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening... (speak now)")
            r.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            except sr.WaitTimeoutError:
                print("Timeout waiting for speech.")
                return None


        google_lang = LANG_TO_GOOGLE.get(lang, "en-IN")
        try:
            text = r.recognize_google(audio, language=google_lang)
            print("You said:", text)
            return text.strip()
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None
        except sr.RequestError as e:
            print("STT request failed:", e)
            return None
    except Exception as e:
        print("Microphone error or no mic available:", e)
        return None