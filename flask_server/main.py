from flask import Flask
from route.router import all_blueprints
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = "./public/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

for bp in all_blueprints:
    app.register_blueprint(bp)


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")
