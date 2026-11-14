"""Turn per-mode runtimes into processed fps and real-time ratio.

Usage:
    python src/benchmark.py --clip /content/sports/examples/soccer/data/clip.mp4
"""
import argparse
import csv
from pathlib import Path

import cv2


def clip_stats(clip: Path) -> tuple[int, float]:
    cap = cv2.VideoCapture(str(clip))
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return frames, fps


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clip", type=Path, required=True)
    parser.add_argument("--timings", type=Path, default=Path("results/timings.csv"))
    parser.add_argument("--out", type=Path, default=Path("results/benchmark.csv"))
    args = parser.parse_args()

    frames, src_fps = clip_stats(args.clip)
    print(f"Clip: {frames} frames at {src_fps:.1f} fps ({frames / src_fps:.1f}s)\n")

    rows = []
    with args.timings.open() as f:
        for t in csv.DictReader(f):
            secs = float(t["seconds"])
            proc_fps = frames / secs if secs and t["status"] == "ok" else 0.0
            ratio = proc_fps / src_fps if src_fps else 0.0
            rows.append({
                "mode": t["mode"],
                "status": t["status"],
                "seconds": secs,
                "processed_fps": round(proc_fps, 2),
                "realtime_ratio": round(ratio, 3),
            })
            print(f"{t['mode']:<22} {proc_fps:6.2f} fps  ({ratio:.2f}x real time)")

    with args.out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nBenchmark written to {args.out}")


if __name__ == "__main__":
    main()
