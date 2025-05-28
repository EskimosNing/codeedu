'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-28 14:20:39
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-28 14:23:12
 # @ Description:
 '''
import os
from pathlib import Path

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path.cwd()))
OUTPUT_DIR =PROJECT_ROOT / "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def scan_output_files():
    output_dir = Path("../output")
    return set(str(f) for f in output_dir.glob("*") if f.is_file())