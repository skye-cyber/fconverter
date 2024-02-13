from docx import Document
import PyPDF2
from gtts import gTTS
import time
import requests
# import io
import os
import glob
import shutil
import pydub
import sys
import traceback
from typing import Iterable, List, TypeVar, Union
from functools import reduce
import subprocess

# os.mkdir('tmp', exist_ok=True)


try:
    import speedtest
except ImportError:
    print("Instead of using 'speedtest', please run:\n  $ sudo apt-get install python3-speedtest-cli")
    sys.exit(-1)

T = TypeVar('T')

global retries
retries = 3


def listify(iterable: Iterable[T]) -> List[T]:
    return list(iterable)


def join_audios(segments: Iterable[Union[pydub.AudioSegment, bytes]]) -> pydub.AudioSegment:
    return reduce(lambda s1, s2: s1 + (isinstance(s2, bytes) and pydub.AudioSegment.silent(duration=1) or s2), segments)


def text_to_speech(text: str, output_file: str) -> None:
    print(f'\033[34m Initializing audio conversion sequence retries = {retries}...\033[0m')
    CHUNK_SIZE: int = 8000

    try:
        st = speedtest.Speedtest()  # get initial network speed
        st.get_best_server()
        download_speed: float = st.download()  # Keep units as bytes
        print(f"\033[32m Conversion sequence initialized start speed \033[36m{download_speed/1_000_000:.2f}Mbps\033[0m")

        try:
            if not os.path.exists('./tmp'):
                os.mkdir('tmp')
            ogg_folder = './tmp/.'
        except Exception:
            pass
        # Split input text into smaller parts and generate individual gTTS objects
        for i in range(0, len(text), CHUNK_SIZE):
            chunk = text[i:i+CHUNK_SIZE]
            tts = gTTS(text=chunk, lang='en', slow=False)
            output_filename = f"{ogg_folder}{'_'.join(chunk.split()[:5])}_{len(chunk)}_chunk.ogg"
            tts.save(output_filename)
        for attempt in range(retries):
            try:
                # Combine generated gTTS objects
                combined_files = glob.glob(f"{ogg_folder}*{'_'.join(['abc', str(len(chunk)), 'chunk'])}_*")
                combined_audio = join_audios([pydub.AudioSegment.from_wav(open(fname, 'rb')) for fname in combined_files])

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
                tb = traceback.extract_tb(sys.exc_info()[2])
                print("\n".join([f"  > {line}" for line in map(str, tb)]))
                time.sleep(5)  # Wait 5 seconds before retrying
        else:
            print(f"\033[33m Text-to-audio conversion has failed after {retries} attempts.\033[0m")

    finally:
        ogg_folder = './tmp/.'
        output_file = f'{output_file}'
        # shutil.move(ogg_folder, output_file)  # Use shutil.move instead of mv for moving directories in python
        try:
            subprocess.run(['mv', f'{ogg_folder}', f'{output_file}'], check=True)
            # If you want to keep the original directory after moving, uncomment the first line and comment out the subprocess.run() line
        except Exception:
            shutil.move(ogg_folder, output_file)
            subprocess.run(['rm', '-r', f'{ogg_folder}'])
        print(f"Final Network Speed: {download_speed/(10**6):.2f} Mbps")


def pdf_to_text(pdf_path):
    print('''Processing the file...\n''')
print(f'\033[32m Initializing pdf to text conversion sequence...\033[0m')
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
        print(f"\033[34m Converting {docx_path} to text...\033[0m")
        doc = Document(docx_path)
        paragraphs = [paragraph.text for paragraph in doc.paragraphs]
        return '\n'.join(paragraphs)
    except Exception as e:
        print(f"\033[31m Something went wrong in docx_to_text():{e}\033[0m")


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
    try:
        text_to_speech(text, output_file)
    except Exception:
        pass


if __name__ == "__main__":
    convert_file_to_mp3('Resume.docx', 'Resume.mp3')