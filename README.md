# broadcast-cv-pipeline

Runs the [roboflow/sports](https://github.com/roboflow/sports) soccer pipeline on a 20-second broadcast clip, measures how fast each stage runs, and records where it breaks.

The point is not a new model. It is to see, stage by stage, what goes wrong when you try to turn broadcast footage into tracking data, and what that means for live use.

## Pipeline stages

| Mode | What it does | Under the hood |
|---|---|---|
| `PITCH_DETECTION` | Finds pitch keypoints | YOLOv8 keypoint model |
| `PLAYER_TRACKING` | Detects and tracks players with IDs | YOLOv8 detection + ByteTrack |
| `TEAM_CLASSIFICATION` | Splits players into teams | SigLIP embeddings → UMAP → KMeans |
| `RADAR` | Projects players onto a top-down pitch | All of the above + homography |

## How to run

Open `notebooks/run_pipeline.ipynb` on a Colab GPU runtime and run the cells top to bottom. It clones roboflow/sports, downloads the pretrained models, trims a 20-second clip, then calls:

```bash
python src/run_modes.py --soccer-dir /content/sports/examples/soccer --clip data/clip.mp4
python src/benchmark.py --clip /content/sports/examples/soccer/data/clip.mp4
```

## Results

Speed: see `results/benchmark.csv`.

Failure modes: see `results/failure_modes.md`.

## What this means for live use

(to write)
