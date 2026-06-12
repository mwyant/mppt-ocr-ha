import os
import cv2
import csv
import argparse
from ocr_adapters import TesseractHostAdapter, TesseractDockerAdapter, TemplateMatchAdapter

def evaluate(image_dir, adapters):
    results = []
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    for filename in image_files:
        # Expecting filename format: <value>_<position>_<timestamp>.jpg
        # e.g. 52.1_bottom_20260612.jpg
        parts = filename.split('_')
        expected = parts[0]
        
        image_path = os.path.join(image_dir, filename)
        img = cv2.imread(image_path)
        if img is None:
            continue

        row = {"filename": filename, "expected": expected}
        
        for name, adapter in adapters.items():
            prediction = adapter.predict(img)
            row[name] = prediction
            row[f"{name}_match"] = (prediction == expected)
            
        results.append(row)
        print(f"Evaluated {filename}: Expected {expected}, Got { {k: v for k, v in row.items() if k in adapters} }")

    return results

def main():
    parser = argparse.ArgumentParser(description="Evaluate OCR adapters against labeled samples")
    parser.add_argument("image_dir", help="Directory containing labeled images")
    parser.add_argument("--out", default="ocr_evaluation.csv", help="Output CSV file")
    parser.add_argument("--docker", action="store_true", help="Include Docker adapter")

    args = parser.parse_args()

    adapters = {
        "tesseract_host": TesseractHostAdapter()
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
