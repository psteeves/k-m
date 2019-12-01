from drive_client.resources import Scraper
from collections import defaultdict
import json


def main():
    scraper = Scraper()

    files = {}
    for resp in scraper.list_drive_files():
        file_id = resp["id"]
        file_content = scraper.get_file_text_content(file_id).decode("utf-8") 
        files[file_id] = file_content
    
    users = defaultdict(list)
    for file_id in files.keys():
        file_permissions = scraper.get_file_permissions(file_id)
        for permission in file_permissions:
            permission_details = scraper.get_permission_details(file_id, permission["id"])
            users[permission_details["emailAddress"]].append({"file_id": file_id, "role": permission_details["role"]})
    
    json.dump(users, open("users.json", "w"), indent=2, sort_keys=True)
    json.dump(files, open("files.json", "w"), indent=2, sort_keys=True)


if __name__ == "__main__":
    main()
