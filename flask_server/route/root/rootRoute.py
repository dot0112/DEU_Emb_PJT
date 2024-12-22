from flask import Blueprint


bp_root = Blueprint("root", __name__)


@bp_root.route("/")
def send_status():
    return "/ ok"
