import requests
import os
import json
import argparse
from datetime import datetime
import time

def capture_snapshot(url, output_dir, stream_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{stream_name}_{timestamp}.jpg"
    filepath = os.path.join(output_dir, filename)
    meta_filepath = os.path.join(output_dir, f"{stream_name}_{timestamp}.json")

    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        duration = time.time() - start_time

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Write image
        with open(filepath, 'wb') as f:
            f.write(response.content)

        # Write metadata
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "url": url,
            "stream": stream_name,
            "filename": filename,
            "size_bytes": len(response.content),
            "content_type": response.headers.get('Content-Type'),
            "duration_seconds": round(duration, 3)
        }

        with open(meta_filepath, 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"Captured snapshot: {filepath} ({len(response.content)} bytes)")
        return filepath

    except Exception as e:
        print(f"Error capturing snapshot: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture a snapshot from go2rtc")
    parser.add_argument("--url", default="http://localhost:1984/api/frame.jpeg?src=mppt", help="Snapshot URL")
    parser.add_argument("--out", default="data/snapshots", help="Output directory")
    parser.add_argument("--stream", default="mppt", help="Stream name for prefixing")

    args = parser.parse_args()
    capture_snapshot(args.url, args.out, args.stream)
