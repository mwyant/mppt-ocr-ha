import os
import requests
import google.generativeai as genai
import json
import time

# Configure Gemini
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash-8b') # Using Flash 8B as a proxy for Flash Lite

def poll_and_parse():
    snapshot_url = "http://localhost:1984/api/frame.jpeg?src=mppt"
    
    try:
        # Fetch snapshot
        response = requests.get(snapshot_url, timeout=10)
        response.raise_for_status()
        
        # Send to Gemini
        prompt = "Read the top and bottom numbers from this display. Return ONLY valid JSON in the format: {\"top\": <int>, \"bottom\": <float>}"
        
        # We need to pass the image data. The SDK expects a file-like object or bytes.
        # Since we have bytes, we can use a wrapper or save to temp file.
        # For simplicity, let's use a temp file.
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name
            
        sample_file = genai.upload_file(tmp_path)
        
        response = model.generate_content([prompt, sample_file])
        
        # Parse JSON
        result = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
        
        # Cleanup
        genai.delete_file(sample_file.name)
        os.remove(tmp_path)
        
        return result
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print(poll_and_parse())
