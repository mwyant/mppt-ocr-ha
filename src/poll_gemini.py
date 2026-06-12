import os
import requests
import json
import base64

def get_api_key():
    with open("/container_mounts/mppt-ocr-ha/.secrets", "r") as f:
        return f.read().strip()

def poll_and_parse():
    snapshot_url = "http://localhost:1984/api/frame.jpeg?src=mppt"
    api_key = get_api_key()
    
    # API endpoint for Gemini 1.5 Flash
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    
    try:
        # Fetch snapshot
        response = requests.get(snapshot_url, timeout=10)
        response.raise_for_status()
        
        # Encode image to base64
        image_b64 = base64.b64encode(response.content).decode('utf-8')
        
        # Prepare request payload
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Read the top and bottom numbers from this display. Return ONLY valid JSON in the format: {\"top\": <int>, \"bottom\": <float>}"},
                    {"inline_data": {"mime_type": "image/jpeg", "data": image_b64}}
                ]
            }]
        }
        
        # Send request with API key header
        headers = {'Content-Type': 'application/json', 'x-goog-api-key': api_key}
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        # Parse JSON
        result_text = response.json()['candidates'][0]['content']['parts'][0]['text']
        result = json.loads(result_text.strip().replace("```json", "").replace("```", ""))
        
        return result
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print(poll_and_parse())
