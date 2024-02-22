import os
import cv2
import pytesseract
from PIL import Image


# Helper function to load image depending upon the format
def load_image(image_path):
    _, ext = os.path.splitext(image_path)
    if ext == '.png':
        return cv2.imread(image_path)
    elif ext == '.jpeg' or ext == '.jpg':
        return cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    else:
        raise ValueError(f"Unsupported image format: {ext}")


def ocr_text_extraction(image_paths, OCR_folder):
    # Check input arguments
    if not isinstance(image_paths, list) or len(image_paths) < 1:
        raise TypeError("Expected a non-empty list of image paths.")

    if not os.path.isdir(OCR_folder):
        os.mkdir(OCR_folder)

    for image_path in image_paths:
        print(f"\033[34mProcessing {image_path}>>>\033[0m")
        try:
            img = load_image(image_path)

            if img is None:
                print(f"Error: Could not open or read the image '{image_path}'.")
                continue

            # Preprocess image for better OCR results
            gray = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
            blurred = cv2.GaussianBlur(gray, (7, 7), 0)
            thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            img_pil = Image.fromarray(thresh)

            # Determine number of pages
            num_pages = int(len(pytesseract.image_to_boxes(img_pil, config='--psm 6 -c tessedit_char_whitelist=0123456789')) / 10)

            for page_num in range(num_pages):
                box = pytesseract.image_to_box_info(img_pil, config='--psm 6 --dpi 300')[page_num]['level']
                x, y, w, h = map(int, box['area'].split('x'))
                roi = img_pil.crop((x, y, w, h))

                # Perform OCR using pytesseract
                text = pytesseract.image_to_string(roi, lang="eng", config="-c tessedit_char_whitelist=0123456789")

                # Save each page as a separate text file
                filename = f"{os.path.basename(image_path).replace('.', '_').replace(' ', '_')}_page_{page_num}.txt"
                file_path = os.path.join(OCR_folder, filename)
                with open(file_path, 'w') as outfile:
                    outfile.write(text)
                    print(f"\033[32mPage {page_num+1} of '{image_path}' saved as '{filename}' >>>\033[0m")

        except Exception as e:
            print(f"Error: Page {page_num+1} of '{image_path}': {str(e)}")


if __name__ == "__main__":
    ocr_text_extraction('/home/user/Pictures/Screenshots/code1.png', 'ocr.txt')