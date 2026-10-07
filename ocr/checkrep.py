import argparse
from pathlib import Path
from llm7shi import detect_repetition

parser = argparse.ArgumentParser(description="Check files for repetition using llm7shi.detect_repetition")
parser.add_argument("files", nargs="+", type=Path, help="Files to check for repetition")

args = parser.parse_args()

repetitive_files = []

for file_path in args.files:
    content = file_path.read_text(encoding='utf-8')
    if detect_repetition(content):
        print(file_path)
        repetitive_files.append(file_path)

if repetitive_files:
    response = input("\nDelete these files? (y/N): ")
    if response.lower() in ['y', 'yes']:
        for file_path in repetitive_files:
            file_path.unlink()
            print(f"Deleted: {file_path}")
