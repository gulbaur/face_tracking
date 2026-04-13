# Face Tracking with DJI Tello EDU Drone

Autonomous real-time face tracking system — the drone detects a specific face and follows it automatically by adjusting its position and rotation.

## How it works

1. The drone streams video in real time
2. Each frame is passed to a custom YOLOv8 model
3. If a face is detected, the drone calculates the offset from the center of the frame
4. Based on the offset, the drone rotates, moves up/down, and adjusts distance automatically

## Project structure

```
├── Face tracking.ipynb      # Dataset prep, model training and validation
├── drone face tracking.py   # Real-time tracking script for the drone
```

## Training

The model was trained in Google Colab on a custom dataset:

- **Dataset:** images of my face, collected and labeled manually
- **Model:** YOLO (fine-tuned via transfer learning)
- **Epochs:** 50
- **Image size:** 640px
- **Class:** `my face`

## Control logic

The drone reacts to face position in the frame:

| Situation | Action |
|---|---|
| Face is to the left | Rotate counter-clockwise |
| Face is to the right | Rotate clockwise |
| Face is above center | Move up |
| Face is below center | Move down |
| Face too small (far away) | Move forward |
| Face too large (close) | Move back |

## Usage

1. Connect to DJI Tello EDU via Wi-Fi
2. Place your trained model at the path specified in the script
3. Run:

```bash
python "drone face tracking.py"
```

Press `Q` to land and exit.
