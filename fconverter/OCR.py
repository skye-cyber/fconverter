import pytesseract
from PIL import Image
import cv2
import numpy as np
import os

# Path to the Tesseract executable (change this if necessary)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def preprocess_image(image):
    # Convert the image to grayscale
    gray_image = image.convert('L')

    # Apply image enhancement techniques (e.g., thresholding, denoising)
    threshold_value = 150
    threshold_image = gray_image.point(lambda p: p > threshold_value and 255)

    denoised_image = cv2.fastNlMeansDenoising(np.array(threshold_image), None, 10, 7, 21)

    return Image.fromarray(denoised_image)


def extract_text(image_path, OCR_file):
    print(f"\033[34mprocessing {image_path}>>>>\033[0m")
    print("\033[36mFound:\n\033[0m")
    try:
        # Validate image file existence
        if not os.path.isfile(image_path):
            raise FileNotFoundError("Image file not found.")

        # Open the image file
        image = Image.open(image_path)

        # Preprocess the image
        preprocessed_image = preprocess_image(image)

        # Perform OCR on the preprocessed image
        text = pytesseract.image_to_string(preprocessed_image)
        print(text)
        current_path = os.getcwd()
        file_path = os.path.join(current_path, OCR_file)
        with open(file_path, 'w') as file:
            file.write(text)
        print("\033[32mGenerating text file for the extracted text>>>\033[0m")
        print(f"File saved in \033[33m{current_path}\033[0m as \033[32m{OCR_file}\033[0m:")
    except Exception as e:
        print(f"Error:>>\033[31m{e}\033[0m")
