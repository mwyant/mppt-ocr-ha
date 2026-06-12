import os
import cv2
import csv
import argparse
from ocr_adapters import TesseractHostAdapter, TesseractDockerAdapter, TemplateMatchAdapter

def evaluate(image_dir, adapters):
    results = []
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    for filename in image_files:
        # Expecting filename format: <top>-<bottom>-mppt_<timestamp>.jpg
        # e.g. 78-0.9-mppt_20260611_161002.jpg
        parts = filename.split('-')
        top = parts[0]
        bottom = parts[1]
        
        image_path = os.path.join(image_dir, filename)
        img = cv2.imread(image_path)
        if img is None:
            continue

        # Crop top and bottom (using same coords as extraction)
        top_crop = {"x": 200, "y": 50, "w": 200, "h": 100}
        bottom_crop = {"x": 200, "y": 150, "w": 200, "h": 100}
        
        top_img = img[top_crop["y"]:top_crop["y"]+top_crop["h"], top_crop["x"]:top_crop["x"]+top_crop["w"]]
        bottom_img = img[bottom_crop["y"]:bottom_crop["y"]+bottom_crop["h"], bottom_crop["x"]:bottom_crop["x"]+bottom_crop["w"]]

        row = {"filename": filename, "expected_top": top, "expected_bottom": bottom}
        
        for name, adapter in adapters.items():
            if name == "template_match":
                row["top_pred"] = adapter.predict(top_img, is_top=True)
                row["bottom_pred"] = adapter.predict(bottom_img, is_top=False)
            else:
                prediction = adapter.predict(img)
                row[name] = prediction
            
        results.append(row)
        print(f"Evaluated {filename}: Expected {top}/{bottom}, Got { {k: v for k, v in row.items() if 'pred' in k} }")

    return results

def main():
    parser = argparse.ArgumentParser(description="Evaluate OCR adapters against labeled samples")
    parser.add_argument("image_dir", help="Directory containing labeled images")
    parser.add_argument("--out", default="ocr_evaluation.csv", help="Output CSV file")
    parser.add_argument("--docker", action="store_true", help="Include Docker adapter")

    args = parser.parse_args()

    adapters = {
        "tesseract_host": TesseractHostAdapter(),
        "template_match": TemplateMatchAdapter()
    }
    if args.docker:
        adapters["tesseract_docker"] = TesseractDockerAdapter()
    
    # Template match is placeholder for now
    # adapters["template_match"] = TemplateMatchAdapter()

    results = evaluate(args.image_dir, adapters)

    if results:
        keys = results[0].keys()
        with open(args.out, 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)
        print(f"Evaluation complete. Results saved to {args.out}")

if __name__ == "__main__":
    main()
