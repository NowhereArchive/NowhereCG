import os
import json
from pathlib import Path

def generate_cg_json(source_path, folder_name, base_url=None):
    if base_url is None:
        base_url = f"https://raw.githubusercontent.com/NowhereArchive/NowhereCGs/main/CGs/{folder_name}"
    
    files = sorted(Path(source_path).iterdir())
    json_array = []
    
    for count, f in enumerate(files, start=1):
        if f.is_file():
            json_array.append({
                "title": str(count),
                "fileName": f"{base_url}/{f.stem}{f.suffix}"
            })
    
    output_path = Path(source_path) / f"{folder_name}.json"
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(json_array, out, indent=2)
    
    print(f"Generated {output_path} with {len(json_array)} entries")

if __name__ == "__main__":
    import sys
    source_path = sys.argv[1]
    folder_name = sys.argv[2]
    base_url = sys.argv[3] if len(sys.argv) > 3 else None
    generate_cg_json(source_path, folder_name, base_url)