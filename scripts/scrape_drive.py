import argparse
import json

from structlog import get_logger

from km.drive_client.resources import Scraper

logger = get_logger()


# TODO fix me! Script is deprecated


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--files-output",
        required=True,
        help="Output file to dump info about files",
    )
    parser.add_argument(
        "-u",
        "--users-output",
        required=True,
        help="Output file to dump info about users",
    )
    parser.add_argument(
        "-m", "--max-num-files", type=int, help="Max number of files to scrape"
    )

    return parser.parse_args()


def run(args):
    scraper = Scraper()

    response = scraper.list_drive_files()
    if args.max_num_files is not None:
        response = response[: args.max_num_files]

    json.dump(
        [f.serialize() for f in response],
        open(args.files_output, "w"),
        indent=2,
        sort_keys=True,
    )
    logger.info(f"File contents saved to {args.files_output}")

    users = scraper.list_users_from_documents(response)
    json.dump(
        [u.serialize() for u in users],
        open(args.users_output, "w"),
        indent=2,
        sort_keys=True,
    )
    logger.info(f"Users with permissions saved to {args.users_output}")


if __name__ == "__main__":
    args = parse_args()
    run(args)
