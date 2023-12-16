import pandas as pd
from docx import Document
import openpyxl


def convert_xls_to_word(xls_file, word_file):
    try:
        # Read the XLS file using pandas
        df = pd.read_excel(xls_file)

        # Create a new Word document
        doc = Document()

        # Iterate over the rows of the dataframe and add them to the Word document
        for _, row in df.iterrows():
            for value in row:
                doc.add_paragraph(str(value))

        # Save the Word document
        doc.save(word_file)
        print("Conversion successful!")
    except Exception as e:
        print("Conversion failed:", str(e))


def convert_xls_to_text(xls_file, text_file):
    try:
        # Read the XLS file using pandas
        workbook = openpyxl.load_workbook(xls_file)
        # Select the first sheet in the workbook
        sheet = workbook.active

        # Convert the sheet to plain text
        text = ""
        for row in sheet.iter_rows(values_only=True):
            text += "".join(str(cell) for cell in row) + "\n"

        # Write the plain text to the output file
        with open(text_file, 'w', encoding='utf-8') as file:
            file.write(text)

        print("Conversion successful!")
    except Exception as e:
        print("Conversion failed:", str(e))
