import argparse
import os
from pdf2docx import parse
import pdfminer.high_level
import re
import traceback
import subprocess
from docx import Document
from pptx import Presentation
from gtts import gTTS


def word_to_pdf(word_file, pdf_file):
    try:
        if os.name == 'posix':  # Check if running on Linux
            subprocess.run(['unoconv', '-f', 'pdf', '-o', pdf_file, word_file])
        else:
            doc = Document(word_file)
            doc.save(pdf_file)
            print(f"Successfully converted {word_file} to {pdf_file}")
    except Exception as e:
        print(f"Error converting {word_file} to {pdf_file}: {e}")
        with open("conversion.log", "a") as log_file:
            log_file.write(f"Error converting {word_file} to {pdf_file}: {e}\n")


def pdf_to_word(pdf_file, word_file):
    try:
        parse(pdf_file, word_file, start=0, end=None)
        return True  # return true if the conversion is successful
        print(f"Successfully converted{pdf_file} to {word_file}")
    except Exception as e:
        print(f"Error converting {pdf_file} to {word_file}: {e}")
        with open("conversion.log", "a") as log_file:
            log_file.write(f"Error converting {pdf_file} to {word_file}:{e}\n")
        return False  # Return False if te conversion fails for all encodings


def word_to_ppt(word_file, ppt_file):
    try:
        document = Document(word_file)
        presentation = Presentation()
        slide_layout = presentation.slide_layouts[1]
        for paragraph in document.paragraphs:
            slide = presentation.slides.add_slide(slide_layout)
            title = slide.shapes.title
            title.text = "Converted Slide"
            content = slide.placeholders[1]
            content.text = paragraph.text
            presentation.save(ppt_file)
            print(f"Successfully converted {word_file} to {ppt_file}")
    except Exception as e:
        print(f"Error converting {word_file} to {ppt_file}: {e}")
        traceback_info = traceback.format_exe()
        with open("conversion.log", "a") as log_file:
            log_file.write(f"Error converting {word_file} to {ppt_file}:\n{traceback_info}\n")


def word_to_txt(word_file, txt_file):
    try:
        doc = Document(word_file)
        with open(txt_file, 'w', encoding='utf-8') as f:
            for paragraph in doc.paragraphs:
                f.write(paragraph.text + '\n')
                print(f"Successfully converted {word_file} to {txt_file}")
    except Exception as e:
        print(f"Error converting {word_file} to {txt_file}: {e}")
        with open("conversion.log", "a") as log_file:
            log_file.write(f"Error converting {word_file} to {txt_file}:{e}\n")


def pdf_to_txt(pdf_file, txt_file):
    try:
        with open(pdf_file, 'rb') as f:
            text = pdfminer.high_level.extract_text(pdf_file)
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(text)
            print(f"Successfully converted {pdf_file} to {txt_file}")
    except Exception as e:
        print(f"Error converting {pdf_file} to {txt_file}: {e}")
        with open("conversion.log", "a") as log_file:
            log_file.write(f"Error converting {pdf_file} to {txt_file}: {e}\n")


def ppt_to_word(ppt_file, word_file):
    try:
        presentation = Presentation(ppt_file)
        document = Document()

        for slide in presentation.slides:
            for shape in slide.shapes:
                if shape.has_text_frame:
                    text_frame = shape.text_frame
                    for paragraph in text_frame.paragraphs:
                        new_paragraph = document.add_paragraph()
                        for run in paragraph.runs:
                            new_run = new_paragraph.add_run(run.text)
                            # Preserve bold formatting
                            new_run.bold = run.font.bold
                            # Preserve italic formatting
                            new_run.italic = run.font.italic
                            # Preserve underline formatting
                            new_run.underline = run.font.underline
                            # Preserve font name
                            new_run.font.name = run.font.name
                            # Preserve font size
                            new_run.font.size = run.font.size
                            try:
                                # Preserve font color
                                new_run.font.color.rgb = run.font.color.rgb
                            except AttributeError:
                                # Ignore error and continue without
                                # setting the font color
                                pass
                    # Add a new paragraph after each slide
                    document.add_paragraph()
        document.save(word_file)
        print(f"Successfully converted {ppt_file} to {word_file}")
    except Exception as e:
        print(f"Error converting {ppt_file} to {word_file}: {e}")
        with open("conversion.log", "a") as log_file:
            log_file.write(f"Error converting {ppt_file} to {word_file}:{e}\n")


def text_to_word(text_file, word_file):
    try:
        # Read the text file
        with open(text_file, 'r', encoding='utf-8', errors='ignore') as file:
            text_content = file.read()

        # Filter out non-XML characters
        filtered_content = re.sub(r'[^\x09\x0A\x0D\x20-\uD7FF\uE000-\uFFFD]+', '', text_content)

        # Create a new Word document
        doc = Document()
        # Add the filtered text content to the document
        doc.add_paragraph(filtered_content)

        # Save the document as a Word file
        doc.save(word_file)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

        print(f"Successfully converted {text_file} to {word_file}")
    except Exception as e:
        print(f"Error converting to Word: {e}\n")


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
        print(f"Sucessfully converted {text_file} to {mp3_file}")
    except Exception as e:
        print(f"An error occurred {e}")

    try:
        # play the audio file
        os.system(f'mvp {mp3_file}')
    except Exception:
        print('''An error has occurred while attempting to play the generated file
            Note that this error is caused by absence of mvp media player in your system ''')


def main():
    parser = argparse.ArgumentParser(description='''Convert files between
                                                 different formats.''')
    parser.add_argument('conversion_type', type=int, help='''The type of
                        conversion to perform (1-7).
                        1: Word to PDF,  2: PDF to Word,  3: Word to PPT,
                        4: Word to TXT,   5: PDF to TXT,    6:PPT to Word,
                        7:TXT to Word     8:TXT to mp3
Note that you must be in the directory where the file to be converted is
located, otherwise you might encounter a directory erro''')

    parser.add_argument('input_file', type=str, help='Name of input file')
    parser.add_argument('output_file', type=str, help='Name of output file')
    args = parser.parse_args()

    if args.conversion_type == 1:
        word_to_pdf(args.input_file, args.output_file)
    elif args.conversion_type == 2:
        pdf_to_word(args.input_file, args.output_file)
    elif args.conversion_type == 3:
        word_to_ppt(args.input_file, args.output_file)
    elif args.conversion_type == 4:
        word_to_txt(args.input_file, args.output_file)
    elif args.conversion_type == 5:
        pdf_to_txt(args.input_file, args.output_file)
    elif args.conversion_type == 6:
        ppt_to_word(args.input_file, args.output_file)
    elif args.conversion_type == 7:
        text_to_word(args.input_file, args.output_file)
    elif args.conversion_type == 8:
        text_to_mp3(args.input_file, args.output_file)
    else:
        print("Invalid conversion type. Please enter a number from 1 to 6.")


if __name__ == '__main__':
    main()
