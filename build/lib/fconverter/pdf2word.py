from pdf2docx import parse


def pdf_to_word(pdf_file, word_file):
    try:
        parse(pdf_file, word_file, start=0, end=None)
        return True  # return true if the conversion is successful
        print(f"\033[1;95m Successfully converted{pdf_file} to {word_file}\033[0m")
    except Exception as e:
        print(f"Error converting {pdf_file} to {word_file}: {e}")
        with open("conversion.log", "a") as log_file:
            log_file.write(f"Error converting {pdf_file} to {word_file}:{e}\n")
        return False  # Return False if te conversion fails for all encodings
