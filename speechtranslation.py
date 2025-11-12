
"""
speechtranslation.py

Menu-driven CLI that supports:
 - Live microphone speech -> speech-to-text -> detect language -> translate
 - Audio file speech -> speech-to-text -> detect language -> translate
 - Typed text -> detect language -> translate
 - Optionally save the translated text to a file

"""

import asyncio
import os
import sys
from typing import Optional

import speech_recognition as sr
from googletrans import Translator


def recognize_from_microphone(timeout: Optional[float] = None, phrase_time_limit: Optional[float] = None) -> str:
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening... (press Ctrl+C to cancel)")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            try:
                print("Recognizing...")
                text = recognizer.recognize_google(audio)
                print(f"Recognized Text: {text}")
                return text
            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
    except KeyboardInterrupt:
        print("\nCancelled by user.")
    except Exception as e:
        print("Microphone error:", e)
    return ""


def recognize_from_file(filepath: str) -> str:
    recognizer = sr.Recognizer()
    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}")
        return ""
    try:
        with sr.AudioFile(filepath) as source:
            print(f"Loading audio file: {filepath}")
            audio = recognizer.record(source)
            try:
                print("Recognizing...")
                text = recognizer.recognize_google(audio)
                print(f"Recognized Text: {text}")
                return text
            except sr.UnknownValueError:
                print("Could not understand the audio in the file.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
    except Exception as e:
        print("Audio file error:", e)
    return ""


async def detect_language_async(text: str) -> Optional[str]:
    translator = Translator()
    try:
        detection = await translator.detect(text)
        # detection.lang is the ISO code
        lang_code = detection.lang if detection and hasattr(detection, "lang") else None
        return lang_code
    except Exception as e:
        print("Language detection error:", e)
        return None


async def translate_async(text: str, dest: str = "en") -> Optional[str]:
    translator = Translator()
    try:
        result = await translator.translate(text, dest=dest)
        translated_text = result.text if result and hasattr(result, "text") else None
        return translated_text
    except Exception as e:
        print("Translation error:", e)
        return None


def detect_language(text: str) -> Optional[str]:
    return asyncio.run(detect_language_async(text))


def translate_text(text: str, dest: str = "en") -> Optional[str]:
    return asyncio.run(translate_async(text, dest))

def save_translation(output_text: str, filename: str) -> bool:
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(output_text)
        return True
    except Exception as e:
        print("Error saving translation:", e)
        return False


def prompt_save_option(translated_text: str):
    choice = input("Save translation to file? (y/N): ").strip().lower()
    if choice == "y":
        default_name = "translation.txt"
        filename = input(f"Enter filename (default '{default_name}'): ").strip()
        if not filename:
            filename = default_name
        ok = save_translation(translated_text, filename)
        if ok:
            print(f"Saved to: {os.path.abspath(filename)}")
        else:
            print("Failed to save file.")

def handle_live_microphone():
    print("\n=== Live Microphone Mode ===")
    text = recognize_from_microphone()
    if not text:
        print("No text recognized.")
        return
    lang = detect_language(text)
    print(f"Detected language: {lang or 'unknown'}")
    dest = input("Enter target language code (default 'en'): ").strip() or "en"
    translated = translate_text(text, dest)
    if translated:
        print(f"\nTranslated Text ({dest}): {translated}")
        prompt_save_option(translated)


def handle_audio_file():
    print("\n=== Audio File Mode ===")
    path = input("Enter path to audio file (wav/flac/...): ").strip()
    if not path:
        print("No file path provided.")
        return
    text = recognize_from_file(path)
    if not text:
        print("No text recognized in audio file.")
        return
    lang = detect_language(text)
    print(f"Detected language: {lang or 'unknown'}")
    dest = input("Enter target language code (default 'en'): ").strip() or "en"
    translated = translate_text(text, dest)
    if translated:
        print(f"\nTranslated Text ({dest}): {translated}")
        prompt_save_option(translated)


def handle_typed_text():
    print("\n=== Typed Text Mode ===")
    text = input("Enter your text: ").strip()
    if not text:
        print("No text provided.")
        return
    lang = detect_language(text)
    print(f"Detected language: {lang or 'unknown'}")
    dest = input("Enter target language code (default 'en'): ").strip() or "en"
    translated = translate_text(text, dest)
    if translated:
        print(f"\nTranslated Text ({dest}): {translated}")
        prompt_save_option(translated)


def show_menu():
    print("\nSpeech & Text Translator - Menu")
    print("1) Live microphone -> translate")
    print("2) Audio file -> translate (wav/flac/...)")
    print("3) Typed text -> translate")
    print("4) Exit")


def main():
    while True:
        show_menu()
        choice = input("Select an option (1-4): ").strip()
        if choice == "1":
            handle_live_microphone()
        elif choice == "2":
            handle_audio_file()
        elif choice == "3":
            handle_typed_text()
        elif choice == "4":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted, exiting.")
        sys.exit(0)
