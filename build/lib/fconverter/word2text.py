from docx import Document


def word_to_txt(word_file, txt_file):
    try:
        doc = Document(word_file)
        with open(txt_file, 'w', encoding='utf-8') as f:
            for paragraph in doc.paragraphs:
                f.write(paragraph.text + '\n')
                print("Processing...")
            print(f"\033[1;95mSuccessfully converted {word_file} to {txt_file}\033[0m")
    except Exception as e:
        print(f"Error converting {word_file} to {txt_file}: {e}")
        with open("conversion.log", "a") as log_file:
            log_file.write(f"Error converting {word_file} to {txt_file}:{e}\n")
