import requests
from pathlib import Path


def capture_and_upload(resultLabel):
    image_path = Path(__file__).parent / "captured_image.jpg"

    if not Path.exists(image_path):
        return

    with open(str(image_path), "rb") as f:
        upload_image(f, resultLabel)


def upload_image(image, resultLabel):
    url = "http://localhost:3000/upload"
    try:
        files = {"images": ("captured_image.py", image, "image/jpeg")}
        response = requests.post(url, files=files, timeout=30)
        response.raise_for_status()
        if response.status_code == 200:
            resultLabel.setText(response.text)
    except requests.exceptions.RequestException as e:
        print(f"오류 발생: {str(e)}")
