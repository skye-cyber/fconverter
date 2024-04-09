from pptx import Presentation
from docx import Document
from PIL import Image
import pytesseract


def get_pptx_files(input_file, output_file):
    if os.path.isfile(input_file):
        word_to_pdf(input_file, output_file)
    elif os.path.isdir(input_file):
        for file in os.listdir(input_file):
            if os.path.isfile(file) and file.endswith('.pptx') or file.endswith('.ppt'):
                input_file = file
                basename, ext = os.path.splitext(input_file)
                output_file = basename + '.docx'
                convert_ppt_to_word(input_file, output_file)
            else:
                pass


def convert_pptx_to_word(ppt_file, docx_file):
    # Load the PowerPoint presentation
    presentation = Presentation(ppt_file)

    # Create a new Word document
    document = Document()

    # Iterate through each slide in the presentation
    for slide_num, slide in enumerate(presentation.slides):
        # Convert the slide to an image
        slide_image = f"slide_{slide_num}.png"
        slide.export(slide_image)

        # Open the image and perform OCR to extract the text
        image = Image.open(slide_image)
        text = pytesseract.image_to_string(image)

        # Add the extracted text to the Word document
        document.add_paragraph(text)

    # Save the Word document
    document.save(docx_file)

# Specify the input PowerPoint file and output Word file


ppt_file = input("Enter ppt file:")
docx_file = 'output.docx'

# Convert the PowerPoint presentation to a Word document
convert_ppt_to_word(ppt_file, docx_file)
