import os
import sys
import cv2
import pytesseract
from PIL import Image
import logging
import logging.handlers

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


def ocr_text_extraction(image_path, OCR_file):
    # Check input arguments
    if not isinstance(image_path, str) or not os.path.exists(image_path) or not os.path.isfile(image_path) or not os.path.isdir(os.path.dirname(image_path)):
        logger.error("Invalid image path.")
        sys.exit(1)

    if not isinstance(OCR_file, str) or not os.path.splitext(OCR_file)[1].lower().endswith(".txt"):
        logger.error("Invalid output file name.")
        sys.exit(1)

    # Load image using OpenCV
    img = cv2.imread(image_path)

    if img is None:
        logger.error("Could not open or find the image.")
        sys.exit(1)

    logger.info(f"\033[34mprocessing {image_path}>>>>\033[0m")

    try:
        # Preprocess image for better OCR results
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        img_pil = Image.fromarray(thresh)

        # Perform OCR using pytesseract
        config = ("-l eng --oem 3 --psm 6")
        text = pytesseract.image_to_string((img_pil), config=config)

        # Remove extra whitespaces and newlines
        # text = ' '.join(text.split()).strip()
        logger.info("\033[36mFound:\n\033[0m")
        print(text)
        current_path = os.getcwd()
        file_path = os.path.join(current_path, OCR_file)
        # Save the extracted text to specified file
        logger.info("\033[32mGenerating text file for the extracted text>>>\033[0m")
        with open(file_path, 'w') as file:
            file.write(text)
        logger.info(f"File saved in \033[33m{current_path}\033[0m as \033[32m{OCR_file}\033[0m:")
    except FileNotFoundError as e:
        logger.error(f"Error: {str(e)}")
    except IOError as e:
        logger.error(f"Error: Could not write to output file '{OCR_file}'. Reason: {str(e)}\033[0m")
    except Exception as e:
        logger.error(f"Error: {type(e).__name__}: {str(e)}")

    return text


if __name__ == "__main__":
    ocr_text_extraction('/home/user/Pictures/Screenshots/Screenshot from 2023-12-13 21-16-00.png', 'ocr.txt')
