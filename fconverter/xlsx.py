import pandas as pd
from docx import Document


def get_xlsx2word_files(input_file, output_file):
    if os.path.isfile(input_file):
        convert_xls_to_word(input_file, output_file)
    elif os.path.isdir(input_file):
        for file in os.listdir(input_file):
            if os.path.isfile(file):
                input_file = file
                if file.endswith('.xlsx'):
                    basename = file[:-4]
                if file.endswith('.xls'):
                    basename = file[:-3]
                output_file = basename + 'docx'
                convert_xls_to_word(input_file, output_file)
            else:
                pass


def get_xlsx2txt_files(input_file, output_file):
    if os.path.isfile(input_file):
        convert_xls_to_text(input_file, output_file)
    elif os.path.isdir(input_file):
        for file in os.listdir(input_file):
            if os.path.isfile(file) and file.endswith('.xlsx') or file.endswith('.xls'):
                input_file = file
                basename, ext = os.path.splitext(input_file)
                output_file = basename + '.txt'
                convert_xls_to_text(input_file, output_file)
            else:
                pass


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
        print("Oops Conversion failed:", str(e))


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
        print("Oops Conversion failed:", str(e))
