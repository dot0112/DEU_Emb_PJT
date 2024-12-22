import numpy as np
import cv2
import queue
from pathlib import Path

haar_path = Path(__file__).parent / "./haarcascade_frontalface_default.xml"

detector = []
semaphor = queue.Queue()


def create_detector():
    global detector
    global haar_path
    for i in range(5):
        detector.append(cv2.CascadeClassifier(haar_path))
        semaphor.put(i)


def predict(image_raw_data):
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


def worker_process(image_path, result_queue):
    try:
        with open(image_path, "rb") as image_file:
            image_raw_data = image_file.read()
            result = predict(image_raw_data)
            print(result)
        result = {"message": f"Image processed successfully: {image_path}"}
        result_queue.put(result)
    except Exception as e:
        result_queue.put({"error": str(e)})
