from docx import Document
import PyPDF2
from gtts import gTTS
import os


def text_to_speech(text, output_file):
    try:
        print("\033[32m Commencing conversion...\033[0m")
        tts = gTTS(text=text, lang='en')
        tts.save(output_file)
        print(
            f'\033[32 Conversion successful. MP3 file saved as {output_file}\033m[0m')
        if True:
            try:

                # play the audio file
                os.system(f'mpv {output_file}')
            except Exception:
                print('''An error has occurred while attempting to play the
                    generated file.>>Note that this error is caused
                    by absence of mvp media player in your system ''')
    except Exception as e:
        print(f"\033[31m Something went wrong:{e}\033[0m")


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
        with open(input_file, 'r', errors='ignore') as file:
            text = file.read().replace('\n', ' ')
        return text
    else:
        print('Unsupported file format. Please provide a PDF or Word document.')
        return

    text_to_speech(text, output_file)
