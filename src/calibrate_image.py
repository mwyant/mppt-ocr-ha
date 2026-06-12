import cv2
import numpy as np
import json
import os
import argparse

def process_image(image_path, config, output_prefix):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image {image_path}")
        return

    # 1. Perspective Correction (if points provided)
    if "perspective_points" in config:
        pts1 = np.float32(config["perspective_points"])
        # Target size for warped image
        width = config.get("warped_width", 800)
        height = config.get("warped_height", 600)
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        img = cv2.warpPerspective(img, M, (width, height))
        cv2.imwrite(f"{output_prefix}_1_warped.jpg", img)

    # 2. Crop
    if "crop" in config:
        c = config["crop"]
        img = img[c["y"]:c["y"]+c["h"], c["x"]:c["x"]+c["w"]]
        cv2.imwrite(f"{output_prefix}_2_cropped.jpg", img)

    # 3. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f"{output_prefix}_3_gray.jpg", gray)

    # 4. Threshold
    thresh_val = config.get("threshold", 127)
    _, thresh = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite(f"{output_prefix}_4_thresh.jpg", thresh)

    print(f"Processed image saved with prefix: {output_prefix}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calibrate and normalize MPPT display image")
    parser.add_argument("image", help="Input image path")
    parser.add_argument("--config", required=True, help="Calibration JSON config")
    parser.add_argument("--out", default="debug_cal", help="Output prefix")

    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = json.load(f)

    process_image(args.image, config, args.out)
