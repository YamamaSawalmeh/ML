import cv2
import pytesseract

def scan_diploma(image_path):
    """
    Scans the diploma image and extracts text using OCR.

    Parameters:
    image_path (str): The path to the diploma image.

    Returns:
    str: Extracted text from the diploma.
    """
    # Load the image from the specified path
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to preprocess the image for better OCR results
    _, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)

    # Use pytesseract to extract text from the processed image
    extracted_text = pytesseract.image_to_string(thresh_image)

    return extracted_text

def save_extracted_data(extracted_text, output_path):
    """
    Saves the extracted text data to a specified output file.

    Parameters:
    extracted_text (str): The text extracted from the diploma.
    output_path (str): The path where the extracted text will be saved.
    """
    with open(output_path, 'w') as file:
        file.write(extracted_text)