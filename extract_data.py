import mediapipe as mp
import cv2
import os
import pickle

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

DATA_DIR = './data'

data = []
labels = []

for dir_ in os.listdir(DATA_DIR):

    class_number = int(dir_)   # تحويل اسم المجلد لرقم

    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):

        img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
        if img is None:
            continue

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                x_, y_ = [], []
                data_aux = []

                # اجمع جميع الإحداثيات
                for lm in hand_landmarks.landmark:
                    x_.append(lm.x)
                    y_.append(lm.y)

                # التطبيع (Normalization)
                min_x = min(x_)
                min_y = min(y_)

                for lm in hand_landmarks.landmark:
                    data_aux.append(lm.x - min_x)
                    data_aux.append(lm.y - min_y)

                # تأكد دائمًا من أن الطول ثابت (21 landmark × 2)
                if len(data_aux) == 42:
                    data.append(data_aux)
                    labels.append(class_number)

# حفظ البيانات
with open('data.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)

print("Training data saved successfully!")
print("Total samples:", len(data))
