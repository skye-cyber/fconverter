from docx import Document
import PyPDF2
from gtts import gTTS
import time
import requests
import speedtest
import io
import os
import shutil
from pydub import AudioSegment


def text_to_speech(text, output_file, retries=3):
    # Initialize variables
    chunk_size = 8000  # Number of characters per chunk
    chunks = []

    # Measure initial network speed
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download()  # Divide by 1000 to get Kbps
    except Exception:
        pass

    print(f'\033[32m Initializing conversion sequence retries = {retries}...\033[0m')
    print(f"\033[32m Conversion in progress...initial speed is \033[36m{download_speed/10**6:.2f}Mbps\033[0m")

    # Split input text into smaller parts and generate individual gTTs objects
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        tts = gTTS(text=chunk, lang='en', slow=False)
        chunks.append(tts)

    for attempt in range(retries):
        try:
            # Combine generated gTTs objects
            combined_audio = AudioSegment.empty()
            for idx, chunk in enumerate(chunks):
                tmp_file = io.BytesIO()
                chunk.write_to_fp(tmp_file)
                chunk_audio = AudioSegment.from_file(tmp_file, format="mp3").set_frame_rate(22050).set_channels(1)
                combined_audio += chunk_audio

            # Save the final audio file
            combined_audio.export(output_file, format="mp3")

            # Print success message and exit the loop
            print(f'\033[32m Conversion successful. MP3 file saved as {output_file}\033[0m')
            break

        # Handle connectivity/network error
        except requests.exceptions.RequestException as e:
            print(f"Network error during conversion attempt {attempt + 1}/{retries}:{e}")
            time.sleep(5)  # Wait 5 seconds before retrying

        # Other exceptions
        except Exception as e:
            print(f'\033[31m Error during conversion attempt {attempt + 1}/{retries}:{e}\033[0m')
            time.sleep(5)  # Wait 5 seconds before retrying
    else:
        print(f"\033[33m Text-to-audio conversion has failed after {retries} attempts.\033[0m")

    return print(f"Final Network Speed: {download_speed/10**6:.2f} Mbps")


def pdf_to_text(pdf_path):
    print('''Processing the file...\n''')
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text += page.extractText()
            return text
    except Exception as e:
        print(f"\033[31m Something went wrong:{e}\033[0m")


def text_file(input_file):
    with open(input_file, 'r', errors='ignore') as file:
        text = file.read().replace('\n', ' ')
    return text


def docx_to_text(docx_path):
    try:
        doc = Document(docx_path)
        paragraphs = [paragraph.text for paragraph in doc.paragraphs]
        return '\n'.join(paragraphs)
    except Exception as e:
        print(f"\033[31m Something went wrong:{e}\033[0m")


def convert_file_to_mp3(input_file, output_file):
    if input_file.endswith('.pdf'):
        text = pdf_to_text(input_file)
    elif input_file.endswith('.docx'):
        text = docx_to_text(input_file)
    elif input_file.endswith('.txt'):
        text = text_file(input_file)
    else:
        print('Unsupported file format. Please provide a PDF or Word document.')
        return

    text_to_speech(text, output_file)
