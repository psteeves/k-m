import argparse
import pickle
from pathlib import Path

from km.constants import DEFAULT_DATABASE_URI, DEFAULT_SERIALIZED_MODELS_DIR
from km.orchestrator.orchestrator import Orchestrator
from km.representations.documents.lda import LDAModel
from km.representations.documents.tf_idf import TFIDFModel


"""
Script to train models. Keyword arguments currently not supported, so default values must be altered in model classes.
Only topic model and keyword models supported for training.
"""


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--model_type",
        choices=["topic", "keyword"],
        required=True,
        help="Type of model to train.",
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
    model_type = args.model_type
    if model_type == "topic":
        model = LDAModel()
    else:
        model = TFIDFModel()
    orchestrator = Orchestrator(db_uri=DEFAULT_DATABASE_URI)
    documents = orchestrator._get_documents()

    model.fit(documents)
    model_path = (args.serialized_model_dir / args.model_name).with_suffix(".pkl")
    pickle.dump(model, open(model_path, "wb"))


if __name__ == "__main__":
    main()
