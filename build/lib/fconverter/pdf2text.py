import pdfminer.high_level


def pdf_to_txt(pdf_file, txt_file):
    try:
        with open(pdf_file, 'rb') as f:
            text = pdfminer.high_level.extract_text(pdf_file)
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(text)
            print(f"\033[1;95mSuccessfully converted {pdf_file} to {txt_file}\033[0m")
    except Exception as e:
        print(f"Error converting {pdf_file} to {txt_file}: {e}")
        with open("conversion.log", "a") as log_file:
            log_file.write(f"Error converting {pdf_file} to {txt_file}: {e}\n")
