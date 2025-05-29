'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-29 19:30:31
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-29 19:31:50
 # @ Description:
 '''
from pathlib import Path
def scan_output_files():
    output_dir = Path("output")
    return set(str(f) for f in output_dir.glob("*") if f.is_file())

def detect_new_files(before: set) -> list:
    after = set(scan_output_files())
    return list(after - before)