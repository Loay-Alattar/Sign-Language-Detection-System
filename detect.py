import pickle
import cv2
import mediapipe as mp
import numpy as np
import json
import os

# ===============================
# Load Model
# ===============================
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# ===============================
# Load Dynamic Labels
# ===============================
LABELS_FILE = "labels.json"

if not os.path.exists(LABELS_FILE):
    raise FileNotFoundError("labels.json not found!")

with open(LABELS_FILE, "r") as f:
    labels_json = json.load(f)

labels_dict = {int(k): v["name"] for k, v in labels_json.items()}

# ===============================
# Video Capture
# ===============================
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ===============================
# Mediapipe Setup
# ===============================
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# ===============================
# Smoothing buffer
# ===============================
smooth_buffer = []
SMOOTH_SIZE = 5

# ===============================
# Sentence / Stable detection
# ===============================
sentence = []
MAX_SENTENCE_WORDS = 12

stable_label = None
stable_count = 0
STABLE_FRAMES_REQUIRED = 12

last_added_label = None
no_hand_frames = 0
NO_HAND_RESET_FRAMES = 15


def enhance(frame):
    """Small sharpen + contrast boost"""
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    return cv2.filter2D(frame, -1, kernel)


def draw_top_bar(frame, words):
    """Draw sentence bar at the top"""
    bar_height = 80
    cv2.rectangle(frame, (0, 0), (frame.shape[1], bar_height), (35, 90, 180), -1)

    sentence_text = " , ".join(words)
    if not sentence_text:
        sentence_text = "Waiting for gesture..."

    cv2.putText(
        frame,
        sentence_text,
        (20, 50),
        cv2.FONT_HERSHEY_DUPLEX,
        1.1,
        (255, 255, 255),
        2
    )


# ===============================
# Main Loop
# ===============================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    H, W, _ = frame.shape
    frame = enhance(frame)

    # Top sentence bar
    draw_top_bar(frame, sentence)

    # System title / instructions
    cv2.putText(frame, "Jadara Team - Sign Language System",
                (40, 120),
                cv2.FONT_HERSHEY_DUPLEX,
                1.0, (0, 255, 255), 2)

    cv2.putText(frame, "Press C to clear chat | Press 0 to exit",
            (20, frame.shape[0] - 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7, (0, 255, 0), 2)

    # Mediapipe processing
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    data_aux = []
    x_, y_ = [], []

    detected_label = None

    if results.multi_hand_landmarks:
        no_hand_frames = 0

        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

            # Collect coordinates
            for lm in hand_landmarks.landmark:
                x_.append(lm.x)
                y_.append(lm.y)

            # Normalize
            min_x = min(x_)
            min_y = min(y_)

            for lm in hand_landmarks.landmark:
                data_aux.append(lm.x - min_x)
                data_aux.append(lm.y - min_y)

        # Ensure correct input size
        if len(data_aux) == 42:
            # Bounding box
            x1 = int(min(x_) * W) - 20
            y1 = int(min(y_) * H) - 20
            x2 = int(max(x_) * W) + 20
            y2 = int(max(y_) * H) + 20

            # Prediction
            prediction = model.predict([np.asarray(data_aux)])
            pred = int(prediction[0])

            smooth_buffer.append(pred)
            if len(smooth_buffer) > SMOOTH_SIZE:
                smooth_buffer.pop(0)

            final_pred = max(set(smooth_buffer), key=smooth_buffer.count)
            predicted_label = labels_dict.get(final_pred, "Unknown")
            detected_label = predicted_label

            # Stable detection logic
            if detected_label == stable_label:
                stable_count += 1
            else:
                stable_label = detected_label
                stable_count = 1

            # Add to sentence only once after gesture becomes stable
            if stable_count == STABLE_FRAMES_REQUIRED:
                if last_added_label != detected_label:
                    sentence.append(detected_label)
                    last_added_label = detected_label

                    if len(sentence) > MAX_SENTENCE_WORDS:
                        sentence.pop(0)

            # Draw result around hand
            cv2.rectangle(frame, (x1, y1), (x2, y2), (30, 30, 30), 2)
            cv2.putText(frame, detected_label,
                        (x1, y1 - 12),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2, (0, 255, 0), 2)

            # Small status under box
            cv2.putText(frame, f"Stable: {stable_count}/{STABLE_FRAMES_REQUIRED}",
                        (x1, y2 + 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255, 255, 0), 2)

    else:
        no_hand_frames += 1

        if no_hand_frames >= NO_HAND_RESET_FRAMES:
            stable_label = None
            stable_count = 0
            smooth_buffer.clear()
            last_added_label = None

    cv2.imshow("Gesture Detection", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('0'):
        break
    elif key == ord('c'):
        sentence.clear()
        stable_label = None
        stable_count = 0
        last_added_label = None
        smooth_buffer.clear()

cap.release()
cv2.destroyAllWindows()