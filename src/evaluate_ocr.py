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

        row = {"filename": filename, "expected_top": top, "expected_bottom": bottom}
        
        for name, adapter in adapters.items():
            prediction = adapter.predict(img)
            # Simple assumption: prediction contains both values, or needs splitting
            # For now, just store raw prediction
            row[name] = prediction
            
        results.append(row)
        print(f"Evaluated {filename}: Expected {top}/{bottom}, Got { {k: v for k, v in row.items() if k in adapters} }")

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
