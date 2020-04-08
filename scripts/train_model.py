import argparse
from pathlib import Path

from km.constants import DEFAULT_DATABASE_URI, DEFAULT_SERIALIZED_MODELS_DIR
from km.orchestrator.orchestrator import Orchestrator
from km.representations.documents.lda import LDAModel


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--num-topics",
        type=int,
        default=20,
        help="Number of topics to detect in LDA model.",
    )
    parser.add_argument(
        "-m", "--model-name", required=True, help="Name of model.",
    )
    parser.add_argument(
        "-d",
        "--serialized-model-dir",
        default=DEFAULT_SERIALIZED_MODELS_DIR,
        type=Path,
        help="Directory to serialize model to.",
    )
    return parser.parse_args()


def main():
    args = _parse_args()
    topic_model = LDAModel(n_components=args.num_topics)
    orchestrator = Orchestrator(db_uri=DEFAULT_DATABASE_URI, document_model=topic_model)

    orchestrator.fit()
    model_path = (args.serialized_model_dir / args.model_name).with_suffix(".pkl")
    orchestrator.serialize_model(model_path)


if __name__ == "__main__":
    main()
