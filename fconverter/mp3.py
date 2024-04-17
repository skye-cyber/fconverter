import logging
import logging.handlers
import math
import os
import sys
import time
import traceback
from typing import Iterable

import pydub
import PyPDF2
import requests
from docx import Document
from gtts import gTTS
from pydub import AudioSegment

logging.basicConfig(level=logging.INFO, format='%(levelname)-4s %(message)s')
logger = logging.getLogger(__name__)

CHUNK_SIZE = 20000

try:
    import speedtest
except ImportError:
    logger.info("Instead of using 'speedtest', please run:\n \
        $ sudo apt-get install python3-speedtest-cli for linux users")
    sys.exit(1)


def get_2mp3_files(input_file):
    if os.path.isfile(input_file):
        ls = ['.txt', '.doc', '.pdf']
        if input_file.lower().endswith(tuple(ls)):
            output_file = input_file[:-4]
        elif input_file.lower().endswith('.docx'):
            output_file = input_file[:-5]
        convert_file_to_mp3(input_file, output_file)
    elif os.path.isdir(input_file):
        for file in os.listdir(input_file):
            # _, ext = os.path.splitext(input_file)
            if file.endswith('.txt') or file.endswith('.pdf') or \
                    file.endswith('.docx') or file.endswith('.doc'):
                input_file = file
                basename, ext = os.path.splitext(input_file)
                output_file = basename
                convert_file_to_mp3(input_file, output_file)
            else:
                pass


class FrameSummary():
    pass


def join_audios(segments: Iterable[bytes], sample_rate: int = 16000) -> AudioSegment:
    """Join multiple audio segments together"""
    chunks = [AudioSegment.from_buffer(segment, frame_rate=sample_rate) for segment in segments]
    return pydub.concat(*chunks)


def text_to_speech(text: str, output_file: str, ogg_folder: str = 'tempfile', retries: int = 3) -> None:
    """Converts given text to speech using Google Text-to-Speech API."""
    try:
        if not os.path.exists(ogg_folder):
            os.mkdir(ogg_folder)

        st = speedtest.Speedtest()  # get initial network speed
        st.get_best_server()
        download_speed: float = st.download()  # Keep units as bytes
        logger.info(f"\033[32m Conversion to mp3 sequence initialized start\
speed \033[36m{download_speed/1_000_000:.2f}Mbps\033[0m")

        for attempt in range(retries):
            try:
                # Split input text into smaller parts and generate individual gTTS objects
                for i in range(0, len(text), CHUNK_SIZE):
                    chunk = text[i:i+CHUNK_SIZE]
                    for i in range(0, math.ceil(len(text)/CHUNK_SIZE)):
                        output_filename = f"{output_file}_{i}.ogg"
                        if os.path.exists(output_filename):
                            output_filename = f"{output_file}_{i+1}.ogg"
                    tts = gTTS(text=chunk, lang='en', slow=False)
                    tts.save(output_filename)

                # Combine generated gTTS objects
                combined_files = sorted(os.listdir(ogg_folder))
                # combined_files = sorted(glob.iglob(ogg_folder+"/*.ogg"))
                combined_audio = join_audios((open(fname, "rb").read() for fname in combined_files))

                # Save the final audio file
                combined_audio.export(output_file + '.mp3', format="mp3")

                # Delete temporary OGG files
                for fname in reversed(list(os.listdir(ogg_folder))):
                    if fname.startswith('chunk'):
                        os.remove(os.path.join(ogg_folder, fname))

                logger.info(f"\033[32m Conversion successful! Output file: {output_file}\033[0m")
                break

            # Handle any network related issue gracefully
            except Exception in (ConnectionError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError) as e:
                # or Exception in (requests.exceptions.RequestException) as e:
                logger.error(f"Sorry boss we are sad to note the following\
connection issue arised: {e} in {attempt+1}/{retries}:")
                time.sleep(5)  # Wait 5 seconds before retrying

            # Handle connectivity/network error
            except requests.exceptions.RequestException as e:
                logger.error(f"{e}")
            except Exception as e:
                logger.error(f'\033[31m Error during conversion attempt {attempt+1}/{retries}:{e}\033[0m')
                tb = traceback.extract_tb(sys.exc_info()[2])
                logger.info("\n".join([f"  > {line}" for line in map(str, tb)]))
                time.sleep(3)  # Wait 5 seconds before retrying
                pass

        if attempt >= retries:
            logger.error(f"Conversion unsuccessful after {retries} attempts.")

    finally:
        st = speedtest.Speedtest()
        logger.info("Done")
        print("Calculating final speed ...")
        logger.info(f"\033[33m Final Network Speed: {st.download()/(10**6):.2f} Mbps\033[0m")


def pdf_to_text(pdf_path):
    logger.info('''Processing the file...\n''')
    logger.info('\033[32m Initializing pdf to text conversion sequence...\033[0m')
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(pdf_reader.pages):
                page = pdf_reader.pages(page_num)
                text += page.extractText()
            return text
    except Exception as e:
        logger.error(f"\033[31m Something went wrong:{e}\033[0m")


def text_file(input_file):
    with open(input_file, 'r', errors='ignore') as file:
        text = file.read().replace('\n', ' ')
    return text


def docx_to_text(docx_path):
    try:
        logger.info(f"\033[34m Converting {docx_path} to text...\033[0m")
        doc = Document(docx_path)
        paragraphs = [paragraph.text for paragraph in doc.paragraphs]
        return '\n'.join(paragraphs)
    except Exception as e:
        logger.error(f"\033[31m Something went wrong in docx_to_text():{e}\033[0m")


def convert_file_to_mp3(input_file, output_file):
    ls = ["doc", "docx"]
    if input_file.endswith('pdf'):
        try:
            text = pdf_to_text(input_file)
        except FileNotFoundError:
            logger.error("File '{}' was not found.".format(input_file))
            sys.exit(1)

    elif input_file.lower().endswith(tuple(ls)):
        try:
            text = docx_to_text(input_file)
        except FileNotFoundError:
            logger.error("File '{}' was not found.".format(input_file))
            sys.exit(1)

        except Exception as e:
            logger.exception("Error converting {} to text: {}".format(input_file, str(e)))
            sys.exit(1)

        except Exception as e:
            logger.exception("Error converting {} to text: {}".format(input_file, str(e)))
            sys.exit(1)

    elif input_file.endswith('txt'):
        try:
            text = text_file(input_file)
        except FileNotFoundError:
            logger.error("File '{}' was not found.".format(input_file))
            sys.exit(1)

    else:
        logger.error('Unsupported file format. Please provide a PDF or Word document.')
        return
    try:
        text_to_speech(text, output_file)
    except Exception:
        pass


if __name__ == "__main__":
    convert_file_to_mp3('Lecture 1 Introduction to Multimedia systems.docx', 'Test')
