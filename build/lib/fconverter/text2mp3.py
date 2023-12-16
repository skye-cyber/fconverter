import os
from gtts import gTTS
from .eSpeak import text_to_mp3_fallback


def text_to_mp3(text_file, mp3_file):
    print('''Working on it...\n
        This may take a while depending on the file size''')
    try:
        # Read the file content
        with open(text_file, 'r', errors='ignore') as file:
            text = file.read().replace('\n', '')
        # Generate the audio file
        tts = gTTS(text, lang='en')
        tts.save(mp3_file)
        print(f"\033[1;95mSucessfully converted {text_file} to {mp3_file}\033[0m")
        print("Generated file size: ", len(mp3_file), 'MB/kb')
    except Exception as e:
        print(f"An error occurred:\n {e}")
        with open("conversion.log", "a") as log_file:
            log_file.write(f"Error converting {text_file} to {mp3_file}: {e}\n")
        try:
            choice = input('''\033[31mDefaulting\033[0m to \033[32mfallback voice\033[0m,
            \033[33m press \033[34m yes\033[0m to \033[31m continue\033[0m else \033[35m enter to \033[36m exit>>\033[32m ''')
            print(f"\033[38;5;226mYou selected \033[34m{choice} \033[0m")
            if choice.lower == "yes":
                text_to_mp3_fallback(text_file, mp3_file)
                return True
            elif choice == "":
                print("Exiting>>>")
        except Exception as e:
            print(f"\033[31mAll conversion optins have failed\033[0m]:{e}")

    if True:
        try:

            # play the audio file
            os.system(f'mpv {mp3_file}')
        except Exception:
            print('''An error has occurred while attempting to play the
                generated file.>>Note that this error is caused
                by absence of mvp media player in your system ''')
