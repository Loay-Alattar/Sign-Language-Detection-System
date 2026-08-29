import os
import cv2
import numpy as np
import sys

gesture_id = sys.argv[1]

DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 1
dataset_size = 100

cap = cv2.VideoCapture(0)

# Force max resolution (try several options)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
cap.set(cv2.CAP_PROP_FPS, 30)

# Skip bad initial frames
for _ in range(15):
    cap.read()

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

def enhance_frame(frame):
    """ Sharpen + Auto contrast """
    # Sharpen filter
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    frame = cv2.filter2D(frame, -1, kernel)

    # Auto brightness/contrast
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.equalizeHist(l)
    lab = cv2.merge((l, a, b))
    frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    return frame

def draw_text(frame):
    cv2.putText(frame, "Jadara Team - Sawan | Jaradat | Mhmad",
                (40, frame.shape[0] - 40),
                cv2.FONT_HERSHEY_DUPLEX,
                1.0, (0, 255, 255), 2)
    return frame


for j in range(number_of_classes):

    class_dir = os.path.join(DATA_DIR, gesture_id)
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)

    print(f'Collecting data for class {j}')
    print('Press "f" to start capturing or "c" to cancel.')

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera error.")
            break

        frame = enhance_frame(frame)
        frame = draw_text(frame)

        cv2.putText(frame, 'Press [F] to take pictures or [C] to close :)',
                    (40, 60), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 0), 2)

        cv2.imshow('frame', frame)

        key = cv2.waitKey(1)
        if key == ord('f'):
            print("Starting capture...")
            break
        elif key == ord('c'):
            cap.release()
            cv2.destroyAllWindows()
            exit()

    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        if not ret:
            break

        frame = enhance_frame(frame)
        frame = draw_text(frame)

        cv2.imshow('frame', frame)
        cv2.imwrite(os.path.join(class_dir, f'{counter}.jpg'), frame)
        counter += 1
        cv2.waitKey(100)

cap.release()
cv2.destroyAllWindows()
