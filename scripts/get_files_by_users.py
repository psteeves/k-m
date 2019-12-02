import argparse
import json
from collections import defaultdict

from drive_client.resources import Scraper
from utils.text_cleaning import decode_string


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


def main():
    args = parser_args()
    scraper = Scraper()

    files = {}
    for resp in scraper.list_drive_files():
        file_id = resp["id"]
        file_content = scraper.get_file_text_content(file_id)
        file_text = decode_string(file_content)
        files[file_id] = file_content

    users = defaultdict(list)
    for file_id in files.keys():
        file_permissions = scraper.get_file_permissions(file_id)
        for permission in file_permissions:
            permission_details = scraper.get_permission_details(
                file_id, permission["id"]
            )
            users[permission_details["emailAddress"]].append(
                {"file_id": file_id, "role": permission_details["role"]}
            )

    json.dump(users, open(args.users_output, "w"), indent=2, sort_keys=True)
    json.dump(files, open(args.files_output, "w"), indent=2, sort_keys=True)


if __name__ == "__main__":
    main()
