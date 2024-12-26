import orjson
import numpy as np
import cv2
import queue
import mediapipe as mp
from pathlib import Path
from keras import models

haar_path = Path(__file__).parent / "./haarcascade_frontalface_default.xml"

detector = []
semaphor = queue.Queue()

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5
)

landmark_spec = mp_drawing.DrawingSpec(
    color=(0, 255, 0), thickness=9, circle_radius=10
)  # 랜드마크 스타일
connection_spec = mp_drawing.DrawingSpec(
    color=(255, 0, 0), thickness=10
)  # 연결선 스타일

class_mapping = None
with open("./route/upload/controller/class_mapping.json", "rb") as f:
    class_mapping = orjson.loads(f.read())


def create_detector():
    global detector
    global haar_path
    mode = "tensor"

    for i in range(10):
        if mode == "haar":
            detector.append(cv2.CascadeClassifier(haar_path))
        elif mode == "tensor":
            detector.append(
                models.load_model("./route/upload/controller/hand_gesture_model.keras")
            )
        semaphor.put(i)


def predict_haar(image_raw_data):
    if len(detector) <= 0:
        create_detector()

    model_index = semaphor.get()

    try:
        nparr = np.frombuffer(image_raw_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        detect_res = detector[model_index].detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        return detect_res
    finally:
        semaphor.put(model_index)


# def predict_tensor(image_raw_data):
#     global class_mapping
#     global hands
#     global detector
#     predicted_class = None
#     if len(detector) <= 0:
#         create_detector()

#     model_index = semaphor.get()

#     try:

#         nparr = np.frombuffer(image_raw_data, np.uint8)
#         image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#         # 이미지 전달 측에서 BGR 이미지를 전달하도록 해야함
#         rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         results = hands.process(rgb_frame)

#         if results.multi_hand_landmarks:
#             for hand_landmarks in results.multi_hand_landmarks:
#                 # 랜드마크 좌표 추출
#                 h, w, _ = image.shape
#                 x_min, y_min = w, h
#                 x_max, y_max = 0, 0

#                 for landmark in hand_landmarks.landmark:
#                     x = int(landmark.x * w)
#                     y = int(landmark.y * h)
#                     x_min = max(0, min(x_min, x))  # 이미지 경계 내로 제한
#                     y_min = max(0, min(y_min, y))
#                     x_max = min(w, max(x_max, x))
#                     y_max = min(h, max(y_max, y))

#                 # 여유 공간 추가 (이미지 크기의 10%)
#                 margin_w = int(w * 0.1)
#                 margin_h = int(h * 0.1)
#                 x_min = max(0, x_min - margin_w)  # 왼쪽으로 확장
#                 y_min = max(0, y_min - margin_h)  # 위쪽으로 확장
#                 x_max = min(w, x_max + margin_w)  # 오른쪽으로 확장
#                 y_max = min(h, y_max + margin_h)  # 아래쪽으로 확장

#                 mp_drawing.draw_landmarks(
#                     image,
#                     hand_landmarks,
#                     mp_hands.HAND_CONNECTIONS,
#                     landmark_drawing_spec=landmark_spec,
#                     connection_drawing_spec=connection_spec,
#                 )

#                 cropped_image = image[y_min:y_max, x_min:x_max]
#                 resized_image = cv2.resize(cropped_image, (224, 224))

#                 normalized_image = resized_image / 255.0

#                 input_tensor = np.expand_dims(normalized_image, axis=0)

#                 prediction = detector[model_index].predict(input_tensor)
#                 predicted_class = class_mapping[np.argmax(prediction)]

#         return predicted_class
#     finally:
#         semaphor.put(model_index)


def predict_tensor(image_raw_data):
    global class_mapping
    global hands
    global detector
    predicted_class = None
    if len(detector) <= 0:
        create_detector()

    model_index = semaphor.get()

    try:

        nparr = np.frombuffer(image_raw_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # 이미지 전달 측에서 BGR 이미지를 전달하도록 해야함
        rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            for hand_landmarks, hand_info in zip(
                results.multi_hand_landmarks, results.multi_handedness
            ):
                confidence = hand_info.classification[
                    0
                ].score  # 각 손의 confidence score
                if confidence <= 0.6:
                    break
                # 랜드마크 좌표 추출
                landmark_points = np.array(
                    [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]
                ).flatten()

                # 랜드마크를 CNN 입력 형식에 맞게 변환
                reshaped_landmarks = landmark_points.reshape(21, 3)[
                    :, :2
                ]  # X, Y 좌표만 사용
                resized_landmarks = cv2.resize(reshaped_landmarks, (32, 32))
                cnn_input = resized_landmarks.reshape(1, 32, 32, 1)

                prediction = detector[model_index].predict(cnn_input)
                category_idx = np.argmax(prediction)
                predicted_class = class_mapping[str(category_idx)]
                print(f"predeicted class: {predicted_class}")
        return predicted_class
    finally:
        semaphor.put(model_index)


def worker_process(
    image_path,
):
    try:
        sending_result = None
        with open(image_path, "rb") as image_file:
            image_raw_data = image_file.read()
            result = predict_tensor(image_raw_data)
        sending_result = {"text": f"{result}"}
        return sending_result
    except Exception as e:
        return {"error": str(e)}
