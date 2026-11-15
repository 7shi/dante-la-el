"""Downloads the PDF of a scan on Internet Archive and renders its pages as NNN.png.

NNN is the PDF page, which is the leaf number of Internet Archive's OCR (`_djvu.xml`,
`iascan.py`), so the page files and the OCR's leaves share their numbers.

    uv run ocr/scripts/iapdf.py https://archive.org/details/ID -o ocr/X
    uv run ocr/scripts/iapdf.py ID -o ocr/X [-d tmp] [--dpi 300] [--first P] [--last P]

The scan is named by its URL (`/details/ID`, `/download/ID/...`) or by its identifier.
The PDF goes to `DIR/ID/ID.pdf` (default `tmp/ID/ID.pdf`, beside the OCR files of
`iascan.py fetch -d tmp`); an interrupted download resumes, and pages already rendered
are skipped. If `DIR/ID/ID_djvu.xml` is there, the PDF's page count is checked against
its leaves. Needs poppler-utils (pdfinfo, pdftoppm).
"""
import argparse
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

BASE = "https://archive.org/download"


def identifier(s):
    """The scan's identifier, from a URL of Internet Archive or the identifier itself."""
    m = re.search(r"archive\.org/(?:details|download)/([^/?#]+)", s)
    return m.group(1) if m else s.strip("/")


def download(url, path):
    """Downloads url to path, resuming a partial file."""
    have = path.stat().st_size if path.exists() else 0
    req = urllib.request.Request(url, headers={"Range": f"bytes={have}-"} if have else {})
    try:
        r = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        if e.code == 416:  # nothing left: already complete
            print(f"{path}: complete")
            return
        raise
    with r:
        if have and r.status != 206:  # the server ignored the range: start again
            have = 0
        total = have + int(r.headers.get("Content-Length", 0))
        with open(path, "ab" if have else "wb") as f:
            done = have
            while chunk := r.read(1 << 20):
                f.write(chunk)
                done += len(chunk)
                print(f"\r{path.name} {done >> 20}/{total >> 20} MB", end="", file=sys.stderr)
    print(file=sys.stderr)


def page_count(pdf):
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True)
    return int(re.search(r"^Pages:\s+(\d+)", out.stdout, re.M).group(1))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("scan", help="the scan's URL on Internet Archive, or its identifier")
    ap.add_argument("-o", "--outdir", type=Path, required=True, help="where NNN.png go")
    ap.add_argument("-d", "--dir", type=Path, default=Path("tmp"),
                    help="the PDF goes to DIR/ID/ID.pdf (default tmp)")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--first", type=int, default=1)
    ap.add_argument("--last", type=int, help="default: the last page of the PDF")
    a = ap.parse_args()

    ident = identifier(a.scan)
    d = a.dir / ident
    d.mkdir(parents=True, exist_ok=True)
    pdf = d / f"{ident}.pdf"
    download(f"{BASE}/{ident}/{ident}.pdf", pdf)

    pages = page_count(pdf)
    xml = d / f"{ident}_djvu.xml"
    if xml.exists():
        leaves = xml.read_text(encoding="utf-8", errors="replace").count("<OBJECT")
        print(f"{pages} pages in the PDF, {leaves} leaves in the OCR")
        if leaves != pages:
            print("WARNING: the page count differs from the OCR's leaves;"
                  " check before using iascan.py pages", file=sys.stderr)
    else:
        print(f"{pages} pages in the PDF")

    a.outdir.mkdir(parents=True, exist_ok=True)
    last = min(a.last or pages, pages)
    for p in range(a.first, last + 1):
        png = a.outdir / f"{p:03d}.png"
        if png.exists():
            continue
        subprocess.run(["pdftoppm", "-r", str(a.dpi), "-f", str(p), "-l", str(p),
                        "-singlefile", "-png", str(pdf), str(png.with_suffix(""))], check=True)
        print(f"\r{a.outdir} {p}/{last}", end="", file=sys.stderr)
    print(file=sys.stderr)
    print(f"{len(list(a.outdir.glob('*.png')))} PNG files in {a.outdir}")


if __name__ == "__main__":
    main()
