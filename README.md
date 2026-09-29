# Sign Language Detection System

A real-time sign language detection system that uses computer vision and machine learning to recognize hand gestures through a camera and display their corresponding meanings as text.

## Overview

The Sign Language Detection System was developed as an academic graduation project at Jadara University. The system is designed to help reduce communication barriers by recognizing hand gestures and translating supported gestures into readable text in real time.

The system captures video through a camera, detects the user's hand, extracts hand landmarks using MediaPipe Hands, and uses a trained machine learning model to classify the detected gesture.

## Features

- User authentication and login
- Real-time camera access and video capture
- Hand detection and landmark extraction
- Real-time gesture classification
- Display of recognized gesture names
- Gesture label and meaning management
- Gesture data collection through the camera
- Hand landmark feature extraction
- Machine learning model training and retraining
- Adding new gestures
- Real-time display of recognized text

## Technologies Used

- **Python** — Main programming language
- **OpenCV** — Camera access, video capture, image processing, and visualization
- **MediaPipe Hands** — Hand detection and extraction of 21 hand landmarks
- **Machine Learning** — Classification of gestures using extracted hand features
- **JSON** — Storage of gesture labels, names, and meanings

## How It Works

The project follows a complete pipeline from gesture data collection to real-time recognition:

```text
Camera
   │
   ▼
Collect Gesture Data
   │
   ▼
Hand Landmark Extraction
   │
   ▼
Feature Dataset
   │
   ▼
Train Machine Learning Model
   │
   ▼
Real-Time Camera Detection
   │
   ▼
Hand Landmark Detection
   │
   ▼
Gesture Classification
   │
   ▼
Recognized Gesture / Text
```

### 1. Gesture Data Collection

The system uses the camera to capture images of hand gestures. Captured samples are organized according to their corresponding gesture IDs and used as training data.

### 2. Hand Landmark Extraction

MediaPipe Hands detects the user's hand and extracts 21 landmarks representing important points such as fingertips and finger joints.

These landmarks are converted into structured features that can be used by the machine learning model.

### 3. Model Training

The extracted features are paired with their corresponding gesture labels and used to train the classification model.

The resulting trained model can then be reused during real-time detection.

### 4. Real-Time Detection

During detection, the system continuously captures camera frames, detects the hand, extracts its landmarks, and passes the resulting features to the trained model.

The predicted gesture is then displayed to the user as text.

## Project Structure

```text
Sign-Language-Detection/
│
├── collect_data.py
├── extract_data.py
├── train_model.py
├── detect.py
├── gesture_manager.py
├── login.py
├── menu.py
├── labels.json
├── requirements.txt
├── README.md
└── .gitignore
```

## File Descriptions

| File | Description |
|------|-------------|
| `collect_data.py` | Collects gesture images using the camera |
| `extract_data.py` | Extracts hand landmark features from collected data |
| `train_model.py` | Trains the machine learning model using extracted features |
| `detect.py` | Performs real-time hand gesture detection |
| `gesture_manager.py` | Manages gesture information and supports adding new gestures |
| `login.py` | Handles user authentication |
| `menu.py` | Provides the main application menu/interface |
| `labels.json` | Stores gesture IDs, names, and meanings |
| `requirements.txt` | Lists the Python dependencies required by the project |

## Installation

### Requirements

- Python 3.x
- A working webcam or external camera
- A Windows, macOS, or Linux environment capable of running the required Python dependencies

### Install Dependencies

Install the required packages using:

```bash
pip install -r requirements.txt
```

## Usage

The general workflow is:

1. Launch the application.
2. Log in using the authorized credentials.
3. Navigate through the main menu.
4. Collect gesture data when adding a new gesture.
5. Extract hand landmark features from the collected data.
6. Train or retrain the machine learning model.
7. Start real-time detection.
8. Perform a supported hand gesture in front of the camera.
9. The system detects the hand and displays the predicted gesture.

## Data and Model Files

The system may generate or use additional files during operation, including:

- Gesture image datasets
- Extracted feature data
- Trained model files
- Gesture labels

Generated datasets and model files are not required to be included in the source-code repository when they are large or can be regenerated through the project's training pipeline.

## Academic Project

**Project:** Sign Language Detection System  
**Type:** Academic / Graduation Project  
**University:** Jadara University  
**Field:** Computer Science / Information Technology

## Future Improvements

Possible future improvements include:

- Expanding the supported gesture vocabulary
- Improving recognition accuracy
- Supporting continuous sign-language sentences
- Adding speech output
- Improving the user interface
- Supporting additional sign languages

## Disclaimer

This project was developed for academic purposes as part of a university graduation project.

The system demonstrates the application of computer vision and machine learning techniques to real-time sign language gesture recognition.
