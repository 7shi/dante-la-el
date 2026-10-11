import argparse
import statistics
import sys
from pathlib import Path


def quartiles(data):
    return statistics.quantiles(data, n=4, method="inclusive")


def upper_fence(data):
    """箱ひげ図の上側のひげ端。これを超えると外れ値。"""
    if len(data) < 4:
        return None
    q1, _, q3 = quartiles(data)
    return q3 + 1.5 * (q3 - q1)


def main():
    parser = argparse.ArgumentParser(
        description="ファイルサイズ・行数の上振れした外れ値（箱ひげ図の1.5×IQR基準）を表示する"
    )
    parser.add_argument("files", nargs="+", type=Path, help="検査するファイル")
    args = parser.parse_args()

    stats = {}  # path -> (size, nlines)
    for file_path in args.files:
        try:
            text = file_path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"Error: {file_path}: {e}", file=sys.stderr)
            continue
        stats[file_path] = (len(text.encode("utf-8")), len(text.splitlines()))

    outlier_files = set()

    for label, values in (
        ("size", {p: s for p, (s, _) in stats.items()}),
        ("lines", {p: n for p, (_, n) in stats.items()}),
    ):
        data = list(values.values())
        high = upper_fence(data)
        if high is None:
            continue
        print(
            f"{label}: q1={quartiles(data)[0]:.1f} "
            f"median={statistics.median(data):.1f} "
            f"q3={quartiles(data)[2]:.1f} "
            f"upper fence={high:.1f}"
        )
        for path, value in values.items():
            if value > high:
                print(f"  outlier {label}: {path} = {value}")
                outlier_files.add(path)

    outlier_files = sorted(outlier_files)
    print(f"\n{len(outlier_files)} / {len(stats)} files have outliers")
    for path in outlier_files:
        print(path)

    if outlier_files:
        sys.exit(1)


if __name__ == "__main__":
    main()
