import argparse
import json
from collections import defaultdict

from structlog import get_logger

from km.drive_client.resources import Scraper
from km.nlp.text_cleaning import (decode_string, replace_unicode_quotations,
                                  strip_whitespace)

logger = get_logger()


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

    return parser.parse_args()


def main(args):
    scraper = Scraper()

    files = {}
    users = defaultdict(list)
    for resp in scraper.list_drive_files():
        # Get file contents
        file_id = resp["id"]
        file_content = scraper.get_file_text_content(file_id)
        file_text = strip_whitespace(
            replace_unicode_quotations(decode_string(file_content))
        )

        files[file_id] = file_text

        # Get file permisssions
        file_permissions = scraper.get_file_permissions(file_id)
        for permission in file_permissions:
            users[permission["emailAddress"]].append(
                {"file_id": file_id, "role": permission["role"]}
            )

    json.dump(users, open(args.users_output, "w"), indent=2, sort_keys=True)
    json.dump(files, open(args.files_output, "w"), indent=2, sort_keys=True)

    logger.info(
        f"File, user contents saved to {args.files_output}, {args.users_output}"
    )


if __name__ == "__main__":
    args = parse_args()
    main(args)
