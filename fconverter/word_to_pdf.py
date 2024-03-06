import os
import subprocess
from docx import Document


def get_word2pdf_files(input_file, output_file):
    if os.path.isfile(input_file):
        word_to_pdf(input_file, output_file)
    elif os.path.isdir(input_file):
        for file in os.listdir(input_file):
            if os.path.isfile(file) and file.endswith('.docx') or file.endswith('.doc'):
                input_file = file
                basename, ext = os.path.splitext(input_file)
                output_file = basename + '.pdf'
                word_to_pdf(input_file, output_file)
            else:
                pass


def word_to_pdf(word_file, pdf_file):
    try:
        print(f'\033[34mConverting: \033[0m{word_file} \033[34mto \033[0m{pdf_file}')
        if os.name == 'posix':  # Check if running on Linux
            subprocess.run(['soffice', '--convert-to', 'pdf', word_file, pdf_file])
            # print(f"\033[1;95m Successfully converted {word_file} to {pdf_file}\033[0m")
        else:
            doc = Document(word_file)
            doc.save(pdf_file)
            print(f"\033[1;95m Successfully converted {word_file} to {pdf_file}\033[0m")
    except Exception as e:
        print(f"Error converting {word_file} to {pdf_file}: {e}")
        with open("conversion.log", "a") as log_file:
            log_file.write(f"Error converting {word_file} to {pdf_file}: {e}\n")


if __name__ == '__main__':
    get_files('/home/user/Documents/test/', 'none.pdf')
