import os
import sys
import subprocess


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
            # Use subprocess to run the dpkg and grep commands
            result = subprocess.run(['dpkg', '-l', 'libreoffice'], stdout=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print("Please install libreoffice to use this functionality !")
                sys.exit(1)
            subprocess.run(['soffice', '--convert-to', 'pdf', word_file, pdf_file])
            # print(f"\033[1;95m Successfully converted {word_file} to {pdf_file}\033[0m")
        elif os.name == "nt":
            try:
                from docx2pdf import convert
            except ImportError:
                print("Run pip install docx2pdf for this function to work")
                sys.exit(1)
            convert(word_file, pdf_file)
            print(f"\033[1;95m Successfully converted {word_file} to {pdf_file}\033[0m")

    except Exception as e:
        print(f"Error converting {word_file} to {pdf_file}: {e}")
        with open("conversion.log", "a") as log_file:
            log_file.write(f"Error converting {word_file} to {pdf_file}: {e}\n")


if __name__ == '__main__':
    get_word2pdf_files('/home/user/Documents/test/', 'none.pdf')
