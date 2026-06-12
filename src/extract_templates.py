import cv2
import os
import argparse
import numpy as np

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

        # Save templates (simple naming for now, will need manual review)
        cv2.imwrite(os.path.join(output_dir, "top", f"{top_val}_{filename}"), top_img)
        cv2.imwrite(os.path.join(output_dir, "bottom", f"{bottom_val}_{filename}"), bottom_img)

if __name__ == "__main__":
    # Placeholder coordinates - will need adjustment
    top_crop = {"x": 200, "y": 50, "w": 200, "h": 100}
    bottom_crop = {"x": 200, "y": 150, "w": 200, "h": 100}
    
    extract_templates("/home/izzy_ai/mppt_data/preprocessed-sample", "/home/izzy_ai/mppt_data/templates", top_crop, bottom_crop)
