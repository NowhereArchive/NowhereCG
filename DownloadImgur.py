#!/usr/bin/env python3
import json
import os
import sys
import time
import urllib.request
from pathlib import Path


def download_images_from_json(json_path: Path, output_base: Path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    folder_name = json_path.stem
    output_dir = output_base / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📁 {folder_name}/ ({len(data)} images)")

    # Fake a real browser to avoid instant 429/403 blocks
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for i, item in enumerate(data, start=1):
        url = item.get("fileName", "").strip()
        if not url:
            print(f"  [{i:02d}] ⚠️  No URL found, skipping")
            continue

        # Preserve original extension, default to .png
        ext = Path(url.split("?")[0]).suffix or ".png"
        filename = f"{i:02d}{ext}"
        dest = output_dir / filename

        try:
            # Build the request with headers
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req) as response, open(dest, "wb") as out_file:
                out_file.write(response.read())
                
            print(f"  [{i:02d}] ✅  {filename}  ←  {url}")
            
            # Crucial: Sleep for 1 second between downloads to prevent Error 429
            time.sleep(1)

        except Exception as e:
            print(f"  [{i:02d}] ❌  Failed to download {url}: {e}")
            # If we still hit a 429, take a longer break
            if "429" in str(e):
                print("     🛑 Hit rate limit. Sleeping for 10 seconds...")
                time.sleep(10)


def main():
    if len(sys.argv) < 2:
        print("Usage: python download_images.py <directory_of_json_files>")
        sys.exit(1)

    input_dir = Path(sys.argv[1]).resolve()
    if not input_dir.is_dir():
        print(f"Error: '{input_dir}' is not a directory.")
        sys.exit(1)

    json_files = sorted(input_dir.glob("*.json"))
    if not json_files:
        print(f"No JSON files found in '{input_dir}'.")
        sys.exit(0)

    print(f"Found {len(json_files)} JSON file(s) in '{input_dir}'")

    output_base = input_dir

    for json_path in json_files:
        download_images_from_json(json_path, output_base)

    print("\n✨ Done!")


if __name__ == "__main__":
    main()