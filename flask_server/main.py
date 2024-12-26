# from flask import Flask
# from route.router import all_blueprints
# from dotenv import load_dotenv
# from multiprocessing import Pool
# import os

# load_dotenv()

# app = Flask(__name__)

# UPLOAD_FOLDER = "./public/uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# for bp in all_blueprints:
#     app.register_blueprint(bp)


# def create_app():
#     app = Flask(__name__)
#     app.config["POOL"] = Pool(processes=10)
#     app.register_blueprint(bp)

#     @app.teardown_appcontext
#     def close_pool(error):
#         app.config["POOL"].close()
#         app.config["POOL"].join()

#     return app


# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True, port=3000, host="0.0.0.0")


from flask import Flask
from route.router import all_blueprints
from dotenv import load_dotenv
from multiprocessing import Pool
import os

load_dotenv()


def create_app():
    app = Flask(__name__)

    # 업로드 폴더 설정
    UPLOAD_FOLDER = "./public/uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    # 프로세스 풀 설정
    app.config["POOL"] = Pool(processes=10)

    # 블루프린트 등록
    for bp in all_blueprints:
        app.register_blueprint(bp)

    return app


def close_pool(error):
    app = Flask(__name__)
    pool = app.config.get("POOL", None)  # 안전한 접근을 위해 get() 사용
    if pool:
        print("Closing pool...")
        pool.close()  # 더 이상 작업 추가 불가
        pool.join()  # 모든 작업이 종료될 때까지 대기
    else:
        print("No pool to close.")


if __name__ == "__main__":
    app = create_app()
    app.teardown_appcontext(close_pool)
    app.run(debug=True, port=3000, host="0.0.0.0")
