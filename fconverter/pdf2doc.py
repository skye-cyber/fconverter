import subprocess
from docx import Document
import logging
import logging.handlers
from draft import progress_show

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


def pdf_to_word(pdf_file, word_file):
    try:
        from PyPDF2 import PdfFileReader
        # Open the pdf file using PyPDF2
        logger.info('Reading pdf..')
        with open(pdf_file, 'rb') as fh:
            reader = PdfFileReader(fh)
            # create a blanks document using python-docx
            doc = Document
            # Add each page content into the Docx document
            for i in range(len(reader.pages)):
                page = reader.pages[i]
                progress_show(reader.pages[i], len(reader.pages))
                logger.info(f'\033[32mPage{i}/{len(reader.pages)}\033[0m')
                text = page.extract_text()  # .replace('\r\n', '\n').strip()
                # para = doc.add_paragraph(text)
                doc.add_paragraph(text)
            # Save the resulting File
            doc.save(word_file)
            logger.info(f"\033[1;95m Successfully converted{pdf_file} to \
{word_file}\033[0m")
    except ImportError:
        logger.info('Failed to import PyPDF2 \033[34mInstalling it\033[0m')
        subprocess.run(['pip', 'install', 'PyPDF2'])
        pdf_to_word(pdf_file, word_file)
    # except Exception as e:
    # print(f'\033[31m{e}\033[0m')


if __name__ == '__main__':
    pdf_to_word('/home/user/Documents/AD.pdf', 'pdf.pdf')
