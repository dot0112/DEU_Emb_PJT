import requests
from pathlib import Path
from PyQt5.QtCore import QThread, pyqtSignal


server_address = "113.198.233.233"


class AIResultThread(QThread):
    result_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, char_queue):
        super().__init__()
        self.char_queue = char_queue

    def run(self):
        image_path = Path(__file__).parent / "../image" / "captured_image.jpg"

        if not Path.exists(image_path):
            return

        self.upload_image(image_path)

    def upload_image(self, image_path):
        url = f"http://{server_address}:3000/upload/image"
        with open(image_path, "rb") as f:
            try:
                files = {"image": ("captured_image.jpg", f, "image/jpeg")}
                response = requests.post(url, files=files, timeout=30)
                response.raise_for_status()
                if response.status_code == 200:
                    json_data = response.json()  # 서버에서 반환된 JSON 데이터
                    if "text" in json_data and json_data["text"] != "None":
                        print(1)
                        self.char_queue.append(json_data["text"])  # 딕셔너리 키로 접근
            except requests.exceptions.RequestException as e:
                self.error_occurred.emit(f"오류 발생: {str(e)}")
