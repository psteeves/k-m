from flask import Blueprint, current_app, jsonify, request

api = Blueprint("api", __name__)


@api.route("/ping", methods=["GET"])
def ping():
    return "pong"


@api.route("/docs", methods=["GET"])
def docs():
    ork = current_app.orchestrator
    num_docs = len(ork._get_documents())
    return f"DB has {num_docs} documents"


@api.route("/query/docs", methods=["GET"])
def query_docs():
    ork = current_app.orchestrator
    query = request.args.get("query")
    limit = request.args.get("limit", 10)
    if not query:
        raise ValueError(f"You must provide a non-empty query. Got `{query}`")

    results = ork.query_documents(str(query), limit)
    results = [doc.serialize() for doc in results]
    return jsonify(results)


@api.route("/query/users", methods=["GET"])
def query_users():
    ork = current_app.orchestrator
    query = request.args.get("query")
    limit = request.args.get("limit")
    if not query:
        raise ValueError(f"You must provide a non-empty query. Got `{query}`")

    results = ork.query_users(str(query), limit)
    results = [user.serialize() for user in results]
    return jsonify(results)


@api.route("/topics", methods=["GET"])
def topics():
    ork = current_app.orchestrator
    return ork.get_topics()
