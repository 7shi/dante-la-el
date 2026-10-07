#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path


def rename_files(directory_path):
    """
    指定したディレクトリのファイルを走査して、
    page_(\d+)(\..+) を {int($1):03d}{$2} に置換する
    """
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"エラー: ディレクトリ '{directory_path}' が存在しません")
        return
    
    if not directory.is_dir():
        print(f"エラー: '{directory_path}' はディレクトリではありません")
        return
    
    pattern = r"page_(\d+)(\..+)"
    renamed_count = 0
    
    for file_path in directory.iterdir():
        if file_path.is_file():
            old_name = file_path.name
            match = re.search(pattern, old_name)
            
            if match:
                page_number = int(match.group(1))
                extension = match.group(2)
                new_name = f"{page_number:03d}{extension}"
                
                new_file_path = file_path.parent / new_name
                
                if new_file_path.exists():
                    print(f"スキップ: '{new_name}' は既に存在します")
                    continue
                
                try:
                    file_path.rename(new_file_path)
                    print(f"リネーム: '{old_name}' -> '{new_name}'")
                    renamed_count += 1
                except OSError as e:
                    print(f"エラー: '{old_name}' のリネームに失敗しました: {e}")
    
    print(f"\n完了: {renamed_count} 個のファイルをリネームしました")


def main():
    if len(sys.argv) != 2:
        print("使用方法: python rename_files.py <ディレクトリパス>")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    rename_files(directory_path)


if __name__ == "__main__":
    main()