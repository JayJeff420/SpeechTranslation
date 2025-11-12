import asyncio
from googletrans import Translator

def get_text_input():
    text = input("Enter your text: ").strip()
    if not text:
        print("No input provided.")
        return None
    return text

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
    text = get_text_input()
    if text:
        target_lang = input("Enter target language code (default 'en'): ").strip()
        if not target_lang:
            target_lang = 'en'
        translate_text(text, target_lang)
