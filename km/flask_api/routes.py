from flask import Blueprint, current_app, jsonify, request
from km.utils import make_document

api = Blueprint("api", __name__)


@api.route("/ping", methods=["GET"])
def ping():
    return "pong"


@api.route("/query/docs", methods=["POST"])
def query_docs():
    ork = current_app.orchestrator
    query = request.get_json()["query"]
    results = ork.query_documents(query=query)
    results = [doc.serialize() for doc in results]
    return jsonify(results)


@api.route("/query/users", methods=["POST"])
def query_users():
    ork = current_app.orchestrator
    query = request.get_json()["query"]

    results = ork.query_users(query=query)
    results = [user.serialize() for user in results]
    return jsonify(results)


@api.route("/describe/doc", methods=["POST"])
def describe_doc():
    ork = current_app.orchestrator
    content = request.get_json()["content"]

    described_document = ork.describe_document(make_document(content=content))
    named_topics = ork.get_named_topics(described_document, min_score=0.05)

    return jsonify(named_topics)


@api.route("/topics", methods=["GET"])
def topics():
    ork = current_app.orchestrator
    return ork.get_topics()
