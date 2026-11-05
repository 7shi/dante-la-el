import argparse

parser = argparse.ArgumentParser(description='Convert PDF to images')
parser.add_argument('input_pdf', help='Input PDF file')
parser.add_argument('-o', '--output-dir', default=None, help='Output directory')
parser.add_argument('--gamma', type=float, default=None, help='Gamma correction value')
parser.add_argument('-s', '--start', type=int, default=1, help='Starting page number for output files (default: 1)')
parser.add_argument('-d', '--digits', type=int, default=None, help='Number of digits for output filenames (default: auto from total pages)')
args = parser.parse_args()

import os, pdf2image
from tqdm import tqdm
from PIL import Image, ImageEnhance

# PDFを画像に変換
pages = pdf2image.convert_from_path(args.input_pdf)

# 出力ディレクトリの指定がない場合は入力 PDF の拡張子を除いた名前
output_dir = args.output_dir or os.path.splitext(args.input_pdf)[0]

# 出力ディレクトリが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# ファイル名の桁数を決定
total_pages = len(pages)
if args.digits is not None:
    digits = args.digits
else:
    digits = max(3, len(str(args.start + total_pages - 1)))

# 各ページを処理
for i, page in enumerate(tqdm(pages, desc="Converting pages"), args.start):
    img = page.convert("RGB")

    # ガンマ補正
    if args.gamma:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(args.gamma)

    # 保存
    output_path = os.path.join(output_dir, f"{i:0{digits}d}.png")
    img.save(output_path, "PNG")
