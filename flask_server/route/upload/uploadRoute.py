from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from multiprocessing import Process, Queue
from .controller.uploadController import worker_process
import os


bp_upload = Blueprint("upload", __name__, url_prefix="/upload")


@bp_upload.route("/")
def send_status():
    return "/upload ok"


@bp_upload.route("/image", methods=["POST"])
def predict_image():
    try:
        if "image" not in request.files:
            return jsonify({"error": "이미지 파일이 없습니다."}), 400

        file = request.files["image"]
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        pool = current_app.config["POOL"]
        result = pool.apply_async(worker_process, args=(file_path,))
        result_data = result.get()

        if "error" in result_data:
            return jsonify({"error": result_data["error"]}), 500
        return jsonify(result_data), 200

    except Exception as e:
        print("Error: ", e)
        return jsonify({"error": str(e)}), 500
