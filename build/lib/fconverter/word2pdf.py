from docx2pdf import convert


def convert_docx_to_pdf(word_file, pdf_file):
    # Convert DOCX to PDF
    convert('word_file', 'pdf_file')


convert_docx_to_pdf("Resume.docx", "Resume.pdf")