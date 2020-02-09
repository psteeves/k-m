from flask import Blueprint
from flask import current_app


api = Blueprint("api", __name__)


@api.route("/api/ping", methods=["GET"])
def ping():
    return "pong"


@api.route("/api/docs", methods=["GET"])
def docs():
    ork = current_app.orchestrator
    num_docs = len(ork._get_documents())
    return f"DB has {num_docs} documents"
