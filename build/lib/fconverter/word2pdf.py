import os
from docx import Document
import subprocess


def word_to_pdf(word_file, pdf_file):
    try:
        if os.name == 'posix':  # Check if running on Linux
            subprocess.run(['unoconv', '-f', 'pdf', '-o', pdf_file, word_file])
        else:
            doc = Document(word_file)
            doc.save(pdf_file)
            print(f"\033[1;95m Successfully converted {word_file} to {pdf_file}\033[0m")
    except Exception as e:
        print(f"Error converting {word_file} to {pdf_file}: {e}")
        with open("conversion.log", "a") as log_file:
            log_file.write(f"Error converting {word_file} to {pdf_file}: {e}\n")
