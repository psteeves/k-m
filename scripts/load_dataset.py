import argparse
import json
import pickle
from pathlib import Path

import tqdm
from structlog import get_logger

from km.constants import DEFAULT_DATABASE_URI
from km.data_models import Document as SimpleDocument
from km.data_models import User as SimpleUser
from km.db.models import Document, User
from km.db.utils import create_table, session_scope
from km.representations.users.topic_concatenator import TopicConcatenator

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
        default=DEFAULT_DATABASE_URI,
        help="URI of SQLite DB to load data to.",
    )
    parser.add_argument(
        "-m",
        "--serialized-model",
        required=True,
        help="Path to serialized model to use",
    )
    return parser.parse_args()


def get_files(path: Path, uri: str) -> None:
    if Path(uri.split("/")[-1]).exists():
        raise RuntimeError("DB already exists.")
    create_table(uri)
    document_representation_model = pickle.load(open(args.serialized_model, "rb"))
    user_representation_model = TopicConcatenator()

    with session_scope(uri) as session:
        documents_dir = path / "documents"
        user_labels_path = path / "user_labels.json"
        doc_paths = [path for path in documents_dir.iterdir()]
        docs = {}
        logger.info(f"Parsing {len(doc_paths)} documents")
        for doc_path in tqdm.tqdm(doc_paths):
            doc_id = int(doc_path.stem)
            doc = json.load(open(doc_path))
            doc_model = Document(
                id=doc_id, title=doc["title"], content=doc["content"], date=doc["date"]
            )
            simple_document = SimpleDocument.from_db_model(doc_model)
            representation = document_representation_model([simple_document])[
                0
            ].representation
            doc_model.representation = representation
            session.add(doc_model)
            docs[doc_id] = doc_model

        user_labels = json.load(open(user_labels_path))
        logger.info(f"Parsing user labels for {len(user_labels)} users")
        for user_id, info in tqdm.tqdm(user_labels.items()):
            user_model = User(
                id=user_id,
                email=info["email"],
                name=info["name"],
                location=info["location"],
                title=info["title"],
                image_path=info["image_path"],
            )
            for doc_id in info["document_ids"]:
                doc = docs[int(doc_id)]
                user_model.documents.append(doc)
            user_model.representation = user_representation_model(
                [SimpleUser.from_db_model(user_model)]
            )[0].representation
            session.add(user_model)

        session.commit()
        logger.info(f"Added users and files to the DB `{args.database_uri}`")


def run(args):
    return get_files(args.dataset_directory, args.database_uri)


if __name__ == "__main__":
    args = _parse_args()
    run(args)
