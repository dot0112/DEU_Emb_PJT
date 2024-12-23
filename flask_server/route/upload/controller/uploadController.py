import numpy as np
import cv2
import queue
import os
from pathlib import Path
from keras import models

haar_path = Path(__file__).parent / "./haarcascade_frontalface_default.xml"

detector = []
semaphor = queue.Queue()


def create_detector():
    global detector
    global haar_path
    mode = os.getenv("mode")

    for i in range(5):
        if mode == "haar":
            detector.append(cv2.CascadeClassifier(haar_path))
        elif mode == "tensor":
            detector.append(models.load_model(os.getenv("model_path"), compile=False))
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


def predict_tensor(image_raw_data):
    if len(detector) <= 0:
        create_detector()

    model_index = semaphor.get()

    try:
        nparr = np.frombuffer(image_raw_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image_resized = cv2.resize(image, (32, 32))
        image_normalized = image_resized / 255.0
        image_batch = np.expand_dims(image_normalized, axis=0)
        prediction = detector[model_index].predict(image_batch)
        predicted_class = np.argmax(prediction)
        return predicted_class
    finally:
        semaphor.put(model_index)


def worker_process(image_path, result_queue):
    try:
        with open(image_path, "rb") as image_file:
            image_raw_data = image_file.read()
            result = predict_haar(image_raw_data)
            print(result)
        result = {"message": f"Image processed successfully: {image_path}"}
        result_queue.put(result)
    except Exception as e:
        result_queue.put({"error": str(e)})
