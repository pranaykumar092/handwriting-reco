import cv2
import numpy as np
import os
from PIL import Image

def preprocess_image(image_path):
    if not os.path.exists(image_path):
        raise ValueError("Image file not found.")
    
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        try:
            pil_img = Image.open(image_path)
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except Exception as e:
            raise ValueError(f"Cannot load image: {e}")
    
    # Resize large images
    h, w = img.shape[:2]
    if w > 1000 or h > 1000:
        scale = min(1000 / w, 1000 / h)
        img = cv2.resize(img, (int(w*scale), int(h*scale)))
    
    # Grayscale + histogram equalization
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    
    # Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Otsu threshold
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Morphology to remove noise
    kernel = np.ones((2,2), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # Save processed image
    base, ext = os.path.splitext(image_path)
    processed_path = f"{base}_processed{ext}"
    cv2.imwrite(processed_path, morph)
    
    return morph, os.path.basename(processed_path)
