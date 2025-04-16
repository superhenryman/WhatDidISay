from PIL import Image
import pytesseract
import io
from ai_handler import generate_debug_response
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def return_image_string(image:bytes) -> str:
    """"
    DO NOT PLACE THE image parameter as a pillow image! This will fuck everything up!
    
    """
    try:
        pil_image = Image.open(io.BytesIO(image))
        return pytesseract.image_to_string(image=pil_image, lang="en")
    except Exception as e:
        print(f"Error in return_image_string(){e}, possible solution: ")
        print(generate_debug_response(e))
        

