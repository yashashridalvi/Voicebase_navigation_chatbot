from text_to_speech import speak, set_language
from speech_to_text import listen
from map_navigattion import get_coordinates, get_route
from googletrans import Translator

translator = Translator()

# -----------------------------------------------------------
# CLEAN LOCATION INPUT (IMPORTANT)
# -----------------------------------------------------------
def clean_location_input(text, lang_key):
    if not text:
        return text

    text = text.lower()

    remove_words = {
        "english": ["to", "from"],
        "hindi": ["से", "तक"],
        "marathi": ["ते", "पर्यंत"]
    }

    for word in remove_words.get(lang_key, []):
        text = text.replace(word, "")

    return text.strip()


# -----------------------------------------------------------
# LANGUAGE SELECTION
# -----------------------------------------------------------
def choose_language():
    speak("WELCOME TO NAVIGATION BOT")
    speak("Choose language. 1 English. 2 Hindi. 3 Marathi", "english")
    choice = input("Enter 1/2/3: ").strip()
    mapping = {"1": "english", "2": "hindi", "3": "marathi"}
    return mapping.get(choice, "english")


# -----------------------------------------------------------
# INPUT MODE
# -----------------------------------------------------------

def choose_input_mode(lang_key):
    prompts = {
        "english": "Do you want to type or speak? Press 1 for type, 2 for speak.",
        "hindi": "आप टाइप करना चाहते हैं या बोलना? टाइप के लिए 1, बोलने के लिए 2 दबाएं।",
        "marathi": "तुम्हाला टाइप करायचे आहे की बोलायचे? टाइपसाठी 1, बोलण्यासाठी 2 दाबा."
    }
    speak(prompts[lang_key], lang_key)
    choice = input("Enter 1 or 2: ").strip()
    return "type" if choice == "1" else "speak"
   
# -----------------------------------------------------------
# GET LOCATION INPUT
# -----------------------------------------------------------
def get_location_input(lang_key, mode, prompt_text):
    speak(prompt_text, lang_key)

    if mode == "type":
        return input(prompt_text + " ").strip()
    else:
        txt = listen(lang="en" if lang_key == "english" else "hi" if lang_key == "hindi" else "mr")
        if not txt:
            speak({
                "english": "I did not hear you. Please type the location.",
                "hindi": "मैंने आपको नहीं सुना। कृपया स्थान टाइप करें।",
                "marathi": "मला ऐकू आले नाही. कृपया ठिकाण टाइप करा."
            }[lang_key], lang_key)
            return input(prompt_text + " ").strip()
        return txt


# -----------------------------------------------------------
# MAIN FUNCTION
# -----------------------------------------------------------
def main():
    lang_key = choose_language()
    set_language(lang_key)

    greet = {
        "english": "Welcome to Voice Navigation Chatbot.",
        "hindi": "वॉइस नेविगेशन चैटबॉट में आपका स्वागत है।",
        "marathi": "व्हॉइस नेव्हिगेशन चॅटबॉटमध्ये आपले स्वागत आहे."
    }
    speak(greet[lang_key], lang_key)

    mode = choose_input_mode(lang_key)

    start_prompt = {
        "english": "Tell me your starting location. Only city name.",
        "hindi": "अपना प्रारंभिक स्थान बताइए। केवल शहर का नाम।",
        "marathi": "तुमचे प्रारंभिक ठिकाण सांगा. फक्त शहराचे नाव."
    }
    start_location = get_location_input(lang_key, mode, start_prompt[lang_key])

    end_prompt = {
        "english": "Now tell me your destination. Only city name.",
        "hindi": "अब अपना गंतव्य बताइए। केवल शहर का नाम।",
        "marathi": "आता तुमचे गंतव्य ठिकाण सांगा. फक्त शहराचे नाव."
    }
    end_location = get_location_input(lang_key, mode, end_prompt[lang_key])

    # CLEAN INPUT
    start_location = clean_location_input(start_location, lang_key)
    end_location = clean_location_input(end_location, lang_key)

    speak({
        "english": "Finding locations.",
        "hindi": "स्थान खोज रहा हूँ।",
        "marathi": "ठिकाण शोधत आहे."
    }[lang_key], lang_key)

    start_coords = get_coordinates(start_location)
    if not start_coords:
        speak({
            "english": f"Sorry, I could not find {start_location}.",
            "hindi": f"क्षमा करें, मैं {start_location} नहीं खोज पाया।",
            "marathi": f"माफ करा, मला {start_location} सापडले नाही."
        }[lang_key], lang_key)
        return

    end_coords = get_coordinates(end_location)
    if not end_coords:
        speak({
            "english": f"Sorry, I could not find {end_location}.",
            "hindi": f"क्षमा करें, मैं {end_location} नहीं खोज पाया।",
            "marathi": f"माफ करा, मला {end_location} सापडले नाही."
        }[lang_key], lang_key)
        return

    speak({
        "english": "Calculating route.",
        "hindi": "रास्ता निकाल रहा हूँ।",
        "marathi": "मार्ग शोधत आहे."
    }[lang_key], lang_key)

    distance, duration, steps = get_route(start_coords, end_coords)

    if distance is None:
        speak({
            "english": "Sorry, route not found.",
            "hindi": "क्षमा करें, मार्ग नहीं मिला।",
            "marathi": "माफ करा, मार्ग सापडला नाही."
        }[lang_key], lang_key)
        return

    summary = {
        "english": f"Distance is {distance:.1f} kilometers. Estimated time {duration:.1f} minutes.",
        "hindi": f"दूरी {distance:.1f} किलोमीटर है। अनुमानित समय {duration:.1f} मिनट है।",
        "marathi": f"अंतर {distance:.1f} किलोमीटर आहे. अंदाजे वेळ {duration:.1f} मिनिटे आहे."
    }
    speak(summary[lang_key], lang_key)

    speak({
        "english": "Do you want step by step directions? Say yes or no.",
        "hindi": "क्या आप कदम दर कदम दिशा चाहते हैं? हाँ या नहीं बताइए।",
        "marathi": "आपण टप्प्याटप्प्याने दिशा पाहू इच्छिता का? होय किंवा नाही सांगा."
    }[lang_key], lang_key)

    ans = listen(lang="en" if lang_key == "english" else "hi" if lang_key == "hindi" else "mr")
    ans = ans.lower() if ans else ""

    yes_words = ["yes", "y", "हाँ", "ha", "haan", "होय", "hoy"]

    if ans in yes_words or ans.startswith("y"):
        speak({
            "english": "Directions may be detailed. Please follow carefully.",
            "hindi": "दिशाएँ विस्तृत हो सकती हैं, कृपया ध्यान से सुनें।",
            "marathi": "दिशा सविस्तर असू शकतात, कृपया लक्षपूर्वक ऐका."
        }[lang_key], lang_key)


        filtered_steps = []

        for step in steps:
            # Remove meaningless repeated steps
            if "straight" in step.lower() and len(step.split()) <= 2:
                continue
            filtered_steps.append(step)

        # Speak filtered directions
        for i, step in enumerate(filtered_steps[:10], 1):
            print(f"{i}. {step}")
            speak(step, lang_key)

    else:
        speak({
            "english": "Okay, not showing directions.",
            "hindi": "ठीक है, निर्देश नहीं दिखा रहा हूँ।",
            "marathi": "ठीक आहे, दिशा दाखवत नाही."
        }[lang_key], lang_key)


# -----------------------------------------------------------
if __name__ == "__main__":
    main()
