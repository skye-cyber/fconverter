import pandas as pd
from docx import Document


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
        df = pd.read_excel(xls_file)

        # Convert the dataframe to plain text
        text = df.to_string(index=False)

        # Write the plain text to the output file
        with open(text_file, 'w') as file:
            file.write(text)

        print("Conversion successful!")
    except Exception as e:
        print("Conversion failed:", str(e))
