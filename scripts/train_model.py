import argparse
from pathlib import Path

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
        default="serialized_models/",
        type=Path,
        help="Name of model.",
    )
    return parser.parse_args()


def main():
    args = _parse_args()
    topic_model = LDAModel(n_components=args.num_topics)
    orchestrator = Orchestrator(document_model=topic_model)

    orchestrator.fit()
    model_path = args.serialized_model_dir / args.model_name
    orchestrator.serialize_model(model_path)


if __name__ == "__main__":
    main()
