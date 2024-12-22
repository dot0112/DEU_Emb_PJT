from flask import Blueprint, request, jsonify
from .controller.requestOpenAI import request_openAI

bp_translate = Blueprint("translate", __name__, url_prefix="/translate")


@bp_translate.route("/")
def send_status():
    return "/translate ok"


@bp_translate.route("/text", methods=["POST"])
def translate_text():
    global api_key
    try:
        data = request.get_json()
        if not data or "korean_text" not in data:
            return jsonify({"error": "JSON 데이터에 'korean_text'가 없습니다."}), 400
        korean_char = data["korean_text"]
        print(f"Received korean_text: {korean_char}")

        translated_text = request_openAI(korean_char)
        print(f"Translated korean_text: {translated_text}")

        return jsonify({"translated_text": translated_text}), 200
    except Exception as e:
        print("Error: ", e)
        return jsonify({"error": str(e)}), 500
