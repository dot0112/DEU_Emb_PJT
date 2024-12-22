import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=8)


def capture_and_upload(char_queue):
    image_path = Path(__file__).parent / "../image" / "captured_image.jpg"

    if not Path.exists(image_path):
        return

    executor.submit(upload_image, image_path, char_queue)


def upload_image(image_path, char_queue):
    url = "http://localhost:3000/upload/image"
    with open(image_path, "rb") as f:
        try:
            files = {"image": ("captured_image.jpg", f, "image/jpeg")}
            response = requests.post(url, files=files, timeout=30)
            response.raise_for_status()
            if response.status_code == 200:
                print(response.json())
                # char_queue.append(response.json().char) -- 현재 사용 불가
        except requests.exceptions.RequestException as e:
            print(f"오류 발생: {str(e)}")
