from flask import Blueprint, current_app, jsonify, request
from km.utils import make_document

api = Blueprint("api", __name__)


@api.route("/ping", methods=["GET"])
def ping():
    return "pong"


@api.route("/query/docs", methods=["GET"])
def query_docs():
    ork = current_app.orchestrator
    query = request.args.get("query")
    limit = request.args.get("limit", 10)
    if not query:
        raise ValueError(f"You must provide a non-empty query. Got `{query}`")

    results = ork.query_documents(query=str(query), max_docs=limit)
    results = [doc.serialize() for doc in results]
    return jsonify(results)


@api.route("/query/users", methods=["GET"])
def query_users():
    ork = current_app.orchestrator
    query = request.args.get("query")
    limit = request.args.get("limit")
    if not query:
        raise ValueError(f"You must provide a non-empty query. Got `{query}`")

    results = ork.query_users(query=str(query), max_users=limit)
    results = [user.serialize() for user in results]
    return jsonify(results)


@api.route("/describe/doc", methods=["GET"])
def describe_doc():
    ork = current_app.orchestrator
    doc = request.args.get("doc")
    if not doc:
        raise ValueError(f"You must provide a non-empty document content. Got `{doc}`")

    global_topics = ork.get_topics()
    document_topic_scores = ork.describe_documents([make_document(content=doc)])[
        0
    ].representation.tolist()
    document_topics = {
        ", ".join(list(global_topics[i].keys())): score
        for i, score in enumerate(document_topic_scores)
    }
    document_topics = {
        topic: score for topic, score in document_topics.items() if score > 0.05
    }
    return jsonify(document_topics)


@api.route("/topics", methods=["GET"])
def topics():
    ork = current_app.orchestrator
    return ork.get_topics()
