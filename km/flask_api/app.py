from flask import Flask
from flask_cors import CORS
from structlog import get_logger

from km.flask_api.config import Config
from km.flask_api.routes import api
from km.orchestrator.orchestrator import Orchestrator

_API_PREFIX = "/api/v1"

logger = get_logger(__name__)


def create_app():
    config = Config()
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(api, url_prefix=_API_PREFIX)
    _register_orchestrator(app)

    CORS(app)
    return app


def _register_orchestrator(app):
    db_uri = app.config["DATABASE_URI"]
    orchestrator = Orchestrator(db_uri=db_uri)
    orchestrator.load_model(app.config["SERIALIZED_MODEL_DIR"] + "/lda_model.pkl")
    app.orchestrator = orchestrator


def main() -> None:
    app = create_app()
    logger.info("Starting API on port 5000")
    app.run(debug=True, port=app.config["PORT"])


if __name__ == "__main__":
    main()
