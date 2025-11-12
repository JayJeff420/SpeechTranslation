import asyncio
import speech_recognition as sr
from googletrans import Translator

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"Recognized Text: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        return ""

async def translate_text_async(text, target_language='en'):
    translator = Translator()
    try:
        translation = await translator.translate(text, dest=target_language)
        print(f"\nTranslated Text ({target_language}): {translation.text}")
        return translation.text
    except Exception as e:
        print("Translation error:", e)
        return None

def translate_text(text, target_language='en'):
    asyncio.run(translate_text_async(text, target_language))

if __name__ == "__main__":
    spoken_text = recognize_speech()
    if spoken_text:
        lang = input("Enter target language code (default 'en'): ").strip()
        if not lang:
            lang = 'en'
        translate_text(spoken_text, lang)
