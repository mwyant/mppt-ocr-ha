import cv2
import os
import numpy as np

def segment_digits(img):
    # The images are already thresholded (black/white), so we can just find contours
    # Ensure it's grayscale for contour detection
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    
    # Threshold again just in case, to ensure binary
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours by x-coordinate
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])
    
    digits = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w > 5 and h > 10: # Filter noise
            digits.append(img[y:y+h, x:x+w])
    return digits

def extract_templates(image_dir, output_dir):
    os.makedirs(os.path.join(output_dir, "top"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "bottom"), exist_ok=True)

    for filename in os.listdir(image_dir):
        if not filename.endswith(".jpg"): continue
        
        # Filename format: <top>-<bottom>-mppt_<timestamp>.jpg
        parts = filename.split('-')
        top_val = parts[0]
        bottom_val = parts[1]
        
        img = cv2.imread(os.path.join(image_dir, filename))
        if img is None: continue

        # Split image in half
        h, w, _ = img.shape
        top_img = img[0:h//2, :]
        bottom_img = img[h//2:h, :]

        # Segment digits
        top_digits = segment_digits(top_img)
        bottom_digits = segment_digits(bottom_img)

        # Save digits
        for i, d in enumerate(top_digits):
            cv2.imwrite(os.path.join(output_dir, "top", f"{top_val}_{i}_{filename}"), d)
        for i, d in enumerate(bottom_digits):
            cv2.imwrite(os.path.join(output_dir, "bottom", f"{bottom_val}_{i}_{filename}"), d)

if __name__ == "__main__":
    extract_templates("/home/izzy_ai/mppt_data/preprocessed-sample", "/home/izzy_ai/mppt_data/templates_segmented_v2")
