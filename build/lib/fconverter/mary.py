import os
import subprocess
import requests


def start_marytts_server():
    # Get the current working directory
    current_dir = os.getcwd()

    # Construct the full path to the marytts folder
    marytts_dir = os.path.join(current_dir, "marytts-master")

    # Construct the full path to the gradlew script
    gradlew_path = os.path.join(marytts_dir, "gradlew")

    # Set the command to start the MaryTTS server
    command = f"{gradlew_path} run"

    try:
        # Start the MaryTTS server using subprocess
        subprocess.Popen(command, shell=True)
        if True:
            print("MaryTTS server started successfully!")
    except Exception as e:
        print("Failed to start MaryTTS server:", str(e))


def generate_speech(text, output_file):
    # Set up the MaryTTS server URL
    marytts_url = "http://localhost:59125/process"

    # Set the desired voice and other parameters
    voice = "cmu-slt-hsmm"  # Replace with the desired voice
    audio_format = "wav"

    # Set the request payload
    payload = {
        "INPUT_TEXT": text,
        "OUTPUT_TYPE": audio_format,
        "LOCALE": "en_US",
        "VOICE": voice
    }

    try:
        # Send the request to the MaryTTS server
        response = requests.get(marytts_url, params=payload)

        # Save the audio output to a file
        with open(output_file, "wb") as file:
            file.write(response.content)
            while True:
                os.system(f'mpv {output_file}')

        print("Speech generated successfully!")
    except Exception as e:
        print("Speech generation failed:", str(e))


start_marytts_server()  # Example usage

text = "Hello, how are you?"
output_file = "/home/user/fconverter/audio.mp3"
generate_speech(text, output_file)
