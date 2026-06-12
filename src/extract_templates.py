import cv2
import os
import argparse
import numpy as np

def segment_digits(img):
    # Simple thresholding to find digit contours
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours by x-coordinate
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])
    
    digits = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w > 5 and h > 10: # Filter noise
            digits.append(img[y:y+h, x:x+w])
    return digits

def extract_templates(image_dir, output_dir, top_crop, bottom_crop):
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

        # Crop top and bottom
        top_img = img[top_crop["y"]:top_crop["y"]+top_crop["h"], top_crop["x"]:top_crop["x"]+top_crop["w"]]
        bottom_img = img[bottom_crop["y"]:bottom_crop["y"]+bottom_crop["h"], bottom_crop["x"]:bottom_crop["x"]+bottom_crop["w"]]

        # Segment digits
        top_digits = segment_digits(top_img)
        bottom_digits = segment_digits(bottom_img)

        # Save digits (this will need manual cleanup to organize into 0-9 folders)
        for i, d in enumerate(top_digits):
            cv2.imwrite(os.path.join(output_dir, "top", f"{top_val}_{i}_{filename}"), d)
        for i, d in enumerate(bottom_digits):
            cv2.imwrite(os.path.join(output_dir, "bottom", f"{bottom_val}_{i}_{filename}"), d)

if __name__ == "__main__":
    # Placeholder coordinates - will need adjustment
    top_crop = {"x": 200, "y": 50, "w": 200, "h": 100}
    bottom_crop = {"x": 200, "y": 150, "w": 200, "h": 100}
    
    extract_templates("/home/izzy_ai/mppt_data/preprocessed-sample", "/home/izzy_ai/mppt_data/templates_segmented", top_crop, bottom_crop)
