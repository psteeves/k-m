from flask import Blueprint, current_app, jsonify, request

from km.utils import make_document

api = Blueprint("api", __name__)


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


@api.route("/add/doc", methods=["POST"])
def add_doc():
    ork = current_app.orchestrator
    params = request.get_json()
    content = params["content"]
    title = params["title"]
    date = params["date"]

    # TODO fix session error

    new_document = ork.create_new_demo_document(title=title, content=content, date=date)
    return jsonify(new_document.serialize())


@api.route("/get/doc", methods=["POST"])
def get_doc():
    ork = current_app.orchestrator
    doc_id = request.get_json()["doc_id"]
    document = ork.get_document(doc_id=doc_id)
    document = ork.get_named_topics(document)
    return jsonify(document.serialize())
