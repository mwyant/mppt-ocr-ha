import os
import requests
import json
import base64
import time
import tempfile
import mysql.connector

def get_secrets():
    with open("/container_mounts/mppt-ocr-ha/.secrets", "r") as f:
        lines = f.readlines()
        return lines[0].strip(), lines[1].strip()

def poll_and_parse():
    snapshot_url = "http://localhost:1984/api/frame.jpeg?src=mppt"
    api_key, db_password = get_secrets()
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
    
    try:
        response = requests.get(snapshot_url, timeout=10)
        response.raise_for_status()
        
        image_b64 = base64.b64encode(response.content).decode('utf-8')
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Read the top and bottom numbers from this display. Return ONLY valid JSON in the format: {\"top\": <int>, \"bottom\": <float>}"},
                    {"inline_data": {"mime_type": "image/jpeg", "data": image_b64}}
                ]
            }]
        }
        
        headers = {'Content-Type': 'application/json', 'x-goog-api-key': api_key}
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result_text = response.json()['candidates'][0]['content']['parts'][0]['text']
        result = json.loads(result_text.strip().replace("```json", "").replace("```", ""))
        
        # Write to Database
        conn = mysql.connector.connect(
            host="172.19.0.3",
            user="mppt_user",
            password=db_password,
            database="mppt_db"
        )
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS readings (id INT AUTO_INCREMENT PRIMARY KEY, top INT, bottom FLOAT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        cursor.execute("INSERT INTO readings (top, bottom) VALUES (%s, %s)", (result['top'], result['bottom']))
        conn.commit()
        cursor.close()
        conn.close()
        
        return result
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    while True:
        result = poll_and_parse()
        if result:
            print(json.dumps(result))
        time.sleep(15)
