import re
from docx import Document


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
    except FileExistsError as e:
        print(f"Error saving the file: {str(e)}")
        print(f"\033[1;95mSuccessfully converted {text_file} to {word_file}\033[0m")
    except Exception as e:
        print(f"Error converting to Word: {e}\n")
        with open("conversion.log", "a") as log_file:
            log_file.write(f"Error converting {text_file} to {word_file}: {e}\n")
