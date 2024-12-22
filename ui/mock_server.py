from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('image')
    if file:
        # 파일 이름 출력
        print(f"파일 업로드 성공: {file.filename}")
        # 가짜 번역 결과 반환
        return jsonify({"result": "이것은 테스트 번역 결과입니다"})
    return jsonify({"result": "업로드 실패"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=3000)
