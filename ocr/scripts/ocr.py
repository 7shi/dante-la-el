import os
import sys
import time
from tqdm import tqdm
from PIL import Image
from llm7shi import generate_content_retry

PROMPT = "Please transcribe the text exactly as it is written, without translating it. Please use $TeX$ to write mathematical equations. Please only return the results, and do not include any comments. If there is no text in the image, output '(blank page)'."

def generate(messages, **kwargs):
    """Generate a response from the model based on the provided messages and parameters."""
    for attempt in range(5, 0, -1):
        response = generate_content_retry(messages, **kwargs)
        if response.text and not response.repetition:
            return response
        if attempt > 1:
            for i in range(5, -1, -1):
                print(f"\rRetrying... {i}s ", end="", flush=True)
                time.sleep(1)
            print()

def process_ocr(image_paths, model, prompt, dry_run=False):
    targets = []
    text_dict = {}
    
    for image_path in image_paths:
        txt = os.path.splitext(image_path)[0] + ".txt"
        if os.path.exists(txt):
            # Read existing txt file
            try:
                with open(txt, "r", encoding="utf-8") as f:
                    text_dict[image_path] = f.read()
            except Exception as e:
                print(f"Error reading {txt}: {e}", file=sys.stderr)
        else:
            targets.append((image_path, txt))

    for image_path, txt in tqdm(targets):
        print(flush=True, file=sys.stderr)
        print(f"Reading {image_path} ...")
        if dry_run:
            continue
        try:
            with Image.open(image_path) as img:
                response = generate(
                    [img, prompt],
                    model=model,
                    show_params=False
                )
            text_dict[image_path] = response.text
            with open(txt, "w") as f:
                f.write(response.text)
            print("\nFile saved:", txt)
        except Exception as e:
            print(e, file=sys.stderr)

    return text_dict

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate RAG evaluation questions from a text file.')
    parser.add_argument('input_files', type=str, nargs='+', help='Input image file paths.')
    parser.add_argument('-m', '--model', type=str, required=True, help='Model name to use for generation.')
    parser.add_argument('-o', '--output', type=str, default=None, help='Output file path.')
    parser.add_argument('-p', '--prompt', type=str, default=PROMPT, help='Prompt for the OCR process.')
    parser.add_argument('--dry', action='store_true', help='Perform a dry run without writing files.')
    args = parser.parse_args()

    text_dict = process_ocr(args.input_files, args.model, args.prompt, args.dry)
    if args.output and not args.dry:
        # Sort by filename and join texts
        sorted_texts = [text_dict[path] for path in sorted(text_dict.keys())]
        text = "\n--------\n\n".join(t.rstrip() + "\n" for t in sorted_texts)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print("Output:", args.output)

if __name__ == "__main__":
    main()
