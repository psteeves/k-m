import argparse
import json
import pickle
from pathlib import Path

import tqdm
from structlog import get_logger

from km.data_models import Document as SimpleDocument
from km.db.models import Document, User
from km.db.utils import create_table, session_scope

logger = get_logger(__file__)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--dataset-directory",
        type=Path,
        required=True,
        help="Directory containing the data to be loaded.",
    )
    parser.add_argument(
        "-u",
        "--database-uri",
        default="sqlite:///km.sqlite",
        help="URI of SQLite DB to load data to.",
    )
    parser.add_argument(
        "-s",
        "--skip-representation",
        action="store_true",
        help="Don't compute and save document representations",
    )
    parser.add_argument(
        "-m",
        "--serialized-model",
        default="serialized_models/lda_model_50.pkl",
        help="Path to serialized model to use",
    )
    return parser.parse_args()


def get_files(path: Path, uri: str) -> None:
    if Path(uri.split("/")[-1]).exists():
        raise RuntimeError("DB already exists.")
    create_table(uri)
    if not args.skip_representation:
        model = pickle.load(open(args.serialized_model, "rb"))
    with session_scope(uri) as session:
        documents_dir = path / "documents"
        user_labels_path = path / "user_labels.json"
        doc_paths = [path for path in documents_dir.iterdir()]
        docs = {}
        logger.info(f"Parsing {len(doc_paths)} documents")
        for doc_path in tqdm.tqdm(doc_paths):
            doc_id = int(doc_path.stem)
            doc = json.load(open(doc_path))
            doc_model = Document(id=doc_id, title=doc["title"], content=doc["content"])
            if not args.skip_representation:
                simple_document = SimpleDocument.from_db_model(doc_model)
                representation = model([simple_document])[0].representation
                doc_model.representation = representation
            session.add(doc_model)
            docs[doc_id] = doc_model

        user_labels = json.load(open(user_labels_path))
        logger.info(f"Parsing user labels for {len(user_labels)} users")
        for user_id, info in tqdm.tqdm(user_labels.items()):
            user_model = User(id=user_id, email=info["email"])
            for doc_id in info["document_ids"]:
                doc = docs[int(doc_id)]
                user_model.documents.append(doc)
            session.add(user_model)

        session.commit()
        logger.info(f"Added users and files to the DB `{args.database_uri}`")


def run(args):
    return get_files(args.dataset_directory, args.database_uri)


if __name__ == "__main__":
    args = _parse_args()
    run(args)
