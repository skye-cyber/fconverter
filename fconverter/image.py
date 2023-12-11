import cv2


def enhance_image(image_path, save_path):
    try:
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            print("Error:Failed to load the image.")
    except Exception as e:
        print(f'''Failed to read the file {image_path}.
              Reason>>>:: {e}''')
    # Resize the image to fit within the screen or window
    max_width = 800
    max_height = 600
    image = resize_image(image, max_width, max_height)

    # Apply brightness adjustment
    enhanced_image = adjust_brightness(image)

    # Apply contrast enhancement
    enhanced_image = enhance_contrast(enhanced_image)

    # Apply sharpening
    enhanced_image = sharpen_image(enhanced_image)

    # Display the original and enhanced images
    cv2.imshow("Original Image", image)
    cv2.imshow("Enhanced Image", enhanced_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    try:
        # save the resulting enhanced image_path
        cv2.imwrite(save_path, enhanced_image)
        print(f"Resulting image saved succesfully in {save_path} ")
    except Exception as e:
        print(f'''Failed to save the image:
            Reason:{e}''')


def resize_image(image, max_width, max_height):
    height, width = image.shape[:2]

    # Calculate the aspect ratio
    aspect_ratio = width / height

    # Resize the image while maintaining the aspect ratio
    if width > max_width or height > max_height:
        if aspect_ratio > 1:
            new_width = max_width
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(new_height * aspect_ratio)

        image = cv2.resize(image, (new_width, new_height))

    return image


def adjust_brightness(image):
    # Convert the image to the LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # Split the LAB image into L, A, and B channels
    l_channel, a, b = cv2.split(lab)

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to the L channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_channel = clahe.apply(l_channel)

    # Merge the enhanced L channel with the original A and B channels
    enhanced_lab = cv2.merge((l_channel, a, b))

    # Convert the LAB image back to the BGR color space
    enhanced_image = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

    return enhanced_image


def enhance_contrast(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply histogram equalization to enhance contrast
    equalized = cv2.equalizeHist(gray)

    # Convert the equalized image back to the BGR color space
    enhanced_image = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)

    return enhanced_image


def sharpen_image(image):
    # Apply unsharp masking for image sharpening
    blurred = cv2.GaussianBlur(image, (0, 0), 3)
    sharpened_image = cv2.addWeighted(image, 1.5, blurred, -0.5, 0)

    return sharpened_image
