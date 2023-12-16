import pandas as pd
from docx import Document


def convert_xlsx_to_word(xls_file, word_file):
    xlsx_file = input("Enter xls file:")
    word_file = "draft.docx"
    try:
        # Read the XLS file using pandas
        df = pd.read_excel(xlsx_file)

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
