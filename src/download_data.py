"""
Data Retrieval Script for India Weather and Air Quality Dataset
Source: https://huggingface.co/datasets/AkshayKarthick/india-weather-air-quality
Retrieval Date: 2026-10-27
"""

import os
import urllib.request
import hashlib
from datetime import datetime

DATASET_BASE_URL = "https://huggingface.co/datasets/AkshayKarthick/india-weather-air-quality/resolve/main/"
FILES_TO_DOWNLOAD = [
    "air_quality_daily.csv",
    "weather_daily.csv",
    "cities.csv",
    "metadata.json",
    "README.md"
]

RAW_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")

def calculate_sha256(filepath):
    """Compute SHA-256 hash of a file for reproducibility and data integrity."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def download_dataset():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    metadata_log = []
    
    print(f"=== Downloading Dataset from {DATASET_BASE_URL} ===")
    print(f"Target Directory: {RAW_DATA_DIR}")
    print(f"Timestamp: {datetime.now().isoformat()}\n")

    for filename in FILES_TO_DOWNLOAD:
        target_path = os.path.join(RAW_DATA_DIR, filename)
        url = DATASET_BASE_URL + filename
        
        print(f"Downloading {filename}...")
        try:
            urllib.request.urlretrieve(url, target_path)
            file_size = os.path.getsize(target_path)
            file_hash = calculate_sha256(target_path)
            print(f"  -> Success: {file_size:,} bytes | SHA-256: {file_hash[:12]}...")
            metadata_log.append({
                "filename": filename,
                "url": url,
                "size_bytes": file_size,
                "sha256": file_hash,
                "download_time": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"  -> Error downloading {filename}: {e}")
            raise e

    print("\nAll files successfully downloaded and verified.")
    return metadata_log

if __name__ == "__main__":
    download_dataset()
