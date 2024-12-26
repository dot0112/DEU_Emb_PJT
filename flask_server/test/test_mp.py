import mediapipe as mp
import cv2

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

image = cv2.imread("1.jpg")
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = hands.process(image_rgb)

if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        # 랜드마크 좌표 추출
        h, w, _ = image.shape
        x_min, y_min = w, h
        x_max, y_max = 0, 0

        for landmark in hand_landmarks.landmark:
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            x_min = max(0, min(x_min, x))  # 이미지 경계 내로 제한
            y_min = max(0, min(y_min, y))
            x_max = min(w, max(x_max, x))
            y_max = min(h, max(y_max, y))

        # 여유 공간 추가 (이미지 크기의 10%)
        margin_w = int(w * 0.1)
        margin_h = int(h * 0.1)
        x_min = max(0, x_min - margin_w)  # 왼쪽으로 확장
        y_min = max(0, y_min - margin_h)  # 위쪽으로 확장
        x_max = min(w, x_max + margin_w)  # 오른쪽으로 확장
        y_max = min(h, y_max + margin_h)  # 아래쪽으로 확장

        # 랜드마크 및 연결선 그리기
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            landmark_drawing_spec=landmark_spec,
            connection_drawing_spec=connection_spec,
        )

        cv2.imwrite("draw_landmark_original.jpg", image)
