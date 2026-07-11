# SIGNOVA — AI-Powered ASL Sign Language Recognition

SIGNOVA is a real-time American Sign Language (ASL) recognition system that runs fully offline. It uses a custom-trained YOLOv11n object detection model to recognize hand signs through a webcam feed, displayed via a lightweight Tkinter desktop interface.

## Key Result
- **98.6% mAP@0.5** on the validation set

## Tech Stack
- **Model:** YOLOv11n (custom-trained)
- **Computer Vision:** OpenCV
- **Language:** Python
- **Interface:** Tkinter (offline desktop app)
- **Optimizer:** AdamW
- **Dataset Management:** Roboflow

## Features
- Real-time hand sign detection via webcam
- Fully offline — no internet or cloud API required
- Lightweight desktop GUI

## Project Structure
SIGNOVA/
├── best.pt                        # Trained YOLOv11n model weights
├── data.yaml                       # Dataset config for training/validation
├── hand_detector.py                 # Core detection logic
├── project_ui.py                    # Tkinter desktop interface
├── img_label_train.py               # Training data labeling script
├── img_label_val.py                 # Validation data labeling script
├── signova_model_training.ipynb      # Model training notebook (Colab)
└── asl_letters.jpg                  # Reference chart of ASL letters

## Setup & Usage

1. Clone the repo:
git clone https://github.com/samikshyashrestha09-ux/signova-asl-recognition.git
cd signova-asl-recognition

2. Install dependencies:
pip install ultralytics opencv-python

3. Run the app:
python project_ui.py

## Model Training
The model was trained using YOLOv11n on a custom-labeled ASL hand sign dataset, sourced and managed via Roboflow. Training was done iteratively across multiple sessions to improve accuracy, achieving a final result of 98.6% mAP@0.5.

The full training process — including dataset setup, training runs, evaluation metrics, and result visualizations (confusion matrix, precision-recall curves, before/after comparison) — is available in [`signova_model_training.ipynb`](./signova_model_training.ipynb).

## Model Details
- **Final mAP@0.5:** 98.6%
- **Architecture:** YOLOv11n (nano)
- **Optimizer:** AdamW
- **Classes:** 26 (A-Z ASL letters)

## Author
Samikshya Shrestha
B.Sc. Computer Science, Hindustan Institute of Technology and Science (HITS)