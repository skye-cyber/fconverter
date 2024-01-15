import os
import cv2
import pytesseract
from PIL import Image


def ocr_text_extraction(image_path, OCR_file):
    # Load image using OpenCV
    img = cv2.imread(image_path)

    if img is None:
        print("Could not open or find the image.")
        return
    # Validate image file existence
    if not os.path.isfile(image_path):
        raise FileNotFoundError("Image file not found.")
    print(f"\033[34mprocessing {image_path}>>>>\033[0m")
    try:
        # Preprocess image for better OCR results
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        img_pil = Image.fromarray(thresh)

        # Perform OCR using pytesseract
        config = ("-l eng --oem 3 --psm 6")
        text = pytesseract.image_to_string((img_pil), config=config)

        # Remove extra whitespaces and newlines
        text = ' '.join(text.split()).strip()
        print("\033[36mFound:\n\033[0m")
        print(text)
        current_path = os.getcwd()
        file_path = os.path.join(current_path, OCR_file)
        with open(file_path, 'w') as file:
            file.write(text)
        print("\033[32mGenerating text file for the extracted text>>>\033[0m")
        print(f"File saved in \033[33m{current_path}\033[0m as \033[32m{OCR_file}\033[0m:")
    except Exception as e:
        print(f"Error:>>\033[31m{e}\033[0m")

    return text
