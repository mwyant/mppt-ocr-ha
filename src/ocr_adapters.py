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
    def __init__(self, templates_dir="/home/izzy_ai/mppt_data/templates"):
        self.templates_dir = templates_dir
        self.top_templates = {}
        self.bottom_templates = {}
        self._load_templates()

    def _load_templates(self):
        for val in os.listdir(os.path.join(self.templates_dir, "top")):
            img = cv2.imread(os.path.join(self.templates_dir, "top", val))
            self.top_templates[val.split('_')[0]] = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        for val in os.listdir(os.path.join(self.templates_dir, "bottom")):
            img = cv2.imread(os.path.join(self.templates_dir, "bottom", val))
            self.bottom_templates[val.split('_')[0]] = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def predict(self, image_np, is_top=True):
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        templates = self.top_templates if is_top else self.bottom_templates
        
        best_match = None
        best_val = -1
        
        for val, template in templates.items():
            if template.shape[0] > gray.shape[0] or template.shape[1] > gray.shape[1]:
                continue
            res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            if max_val > best_val:
                best_val = max_val
                best_match = val
        
        return best_match if best_val > 0.8 else None

if __name__ == "__main__":
    # Simple test if run directly
    import numpy as np
    adapter = TesseractHostAdapter()
    dummy_img = np.zeros((100, 100), dtype=np.uint8)
    print(f"Test prediction (empty image): {adapter.predict(dummy_img)}")
