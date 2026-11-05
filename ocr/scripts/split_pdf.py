import argparse
from pathlib import Path
parser = argparse.ArgumentParser(description="Split PDF into chunks")
parser.add_argument("input_file", type=Path, help="Input PDF file path")
parser.add_argument("--chunk-size", type=int, default=100, help="Pages per chunk (default: 100)")
args = parser.parse_args()

from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader(args.input_file)
total_pages = len(reader.pages)
chunk_size = args.chunk_size
digits = max(3, len(str(total_pages)))

for start in range(0, total_pages, chunk_size):
    writer = PdfWriter()
    last_next = min(start + chunk_size, total_pages)
    for i in range(start, last_next):
        writer.add_page(reader.pages[i])
    output_pdf = f"{args.input_file.stem}-{start+1:0{digits}d}-{last_next:0{digits}d}.pdf"
    with open(output_pdf, "wb") as f:
        writer.write(f)
