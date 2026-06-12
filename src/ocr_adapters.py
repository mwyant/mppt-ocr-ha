import subprocess
import os
import tempfile
import cv2

class OCRAdapter:
    def predict(self, image_np):
        raise NotImplementedError

class TesseractHostAdapter(OCRAdapter):
    def __init__(self, binary_path="tesseract", lang="eng", config="--psm 7"):
        self.binary_path = binary_path
        self.lang = lang
        self.config = config

    def predict(self, image_np):
        # Save to temp file for tesseract
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name
            cv2.imwrite(tmp_path, image_np)

        try:
            cmd = [
                self.binary_path,
                tmp_path,
                "stdout",
                "-l", self.lang,
                "--psm", "7",
                "-c", "tessedit_char_whitelist=0123456789."
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            text = result.stdout.strip()
            return text
        except subprocess.CalledProcessError as e:
            print(f"Tesseract error: {e.stderr}")
            return None
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

class TesseractDockerAdapter(OCRAdapter):
    def __init__(self, image="jitesoft/tesseract-ocr", lang="eng"):
        self.image = image
        self.lang = lang

    def predict(self, image_np):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = os.path.join(tmpdir, "input.png")
            cv2.imwrite(tmp_path, image_np)

            # Map the temp dir into the container
            cmd = [
                "docker", "run", "--rm",
                "-v", f"{tmpdir}:/data",
                self.image,
                "/data/input.png",
                "stdout",
                "-l", self.lang,
                "--psm", "7",
                "-c", "tessedit_char_whitelist=0123456789."
            ]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                return result.stdout.strip()
            except subprocess.CalledProcessError as e:
                print(f"Tesseract Docker error: {e.stderr}")
                return None

class TemplateMatchAdapter(OCRAdapter):
    def __init__(self, templates_dir=None):
        self.templates_dir = templates_dir
        self.templates = {} # Map of '0'-'9' to list of template images
        if templates_dir and os.path.exists(templates_dir):
            self._load_templates()

    def _load_templates(self):
        # Placeholder for loading templates from disk
        pass

    def predict(self, image_np):
        # Placeholder for template matching logic
        # 1. Segment image into digits
        # 2. For each digit, find best matching template
        # 3. Join and return
        return "NotImplemented"

if __name__ == "__main__":
    # Simple test if run directly
    import numpy as np
    adapter = TesseractHostAdapter()
    dummy_img = np.zeros((100, 100), dtype=np.uint8)
    print(f"Test prediction (empty image): {adapter.predict(dummy_img)}")
