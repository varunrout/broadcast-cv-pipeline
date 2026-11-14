"""Run the roboflow/sports soccer pipeline modes on one clip and log runtime per mode.

Usage:
    python src/run_modes.py --soccer-dir /content/sports/examples/soccer --clip data/clip.mp4
"""
import argparse
import csv
import subprocess
import sys
import time
from pathlib import Path

DEFAULT_MODES = ["PITCH_DETECTION", "PLAYER_TRACKING", "TEAM_CLASSIFICATION", "RADAR"]


def run_mode(soccer_dir: Path, clip: Path, out_dir: Path, mode: str, device: str) -> dict:
    out_path = out_dir / f"out_{mode.lower()}.mp4"
    cmd = [
        sys.executable, "main.py",
        "--source_video_path", str(clip),
        "--target_video_path", str(out_path),
        "--device", device,
        "--mode", mode,
    ]
    start = time.time()
    result = subprocess.run(cmd, cwd=soccer_dir, capture_output=True, text=True)
    seconds = round(time.time() - start, 2)
    ok = result.returncode == 0
    if not ok:
        print(f"[{mode}] FAILED\n{result.stderr[-2000:]}", file=sys.stderr)
    return {"mode": mode, "status": "ok" if ok else "failed", "seconds": seconds, "output": str(out_path)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--soccer-dir", type=Path, required=True, help="Path to roboflow/sports/examples/soccer")
    parser.add_argument("--clip", type=Path, required=True, help="Input clip (absolute, or relative to --soccer-dir)")
    parser.add_argument("--out-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--results", type=Path, default=Path("results/timings.csv"))
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--modes", nargs="+", default=DEFAULT_MODES)
    args = parser.parse_args()

    soccer_dir = args.soccer_dir.resolve()
    clip = args.clip if args.clip.is_absolute() else (soccer_dir / args.clip)
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    args.results.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for mode in args.modes:
        row = run_mode(soccer_dir, clip.resolve(), out_dir, mode, args.device)
        print(f"{row['mode']:<22} {row['status']:<7} {row['seconds']}s")
        rows.append(row)

    with args.results.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["mode", "status", "seconds", "output"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nTimings written to {args.results}")


if __name__ == "__main__":
    main()
