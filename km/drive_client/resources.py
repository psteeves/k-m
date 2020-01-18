from collections import defaultdict
from typing import List, Tuple

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

from km.data_models import Document, Permission, User
from km.nlp.text_cleaning import (
    decode_string,
    replace_unicode_quotations,
    strip_whitespace,
)

SCOPES = "https://www.googleapis.com/auth/drive"
SUPPORTED_MIMETYPES = [
    "application/vnd.google-apps." + ext for ext in ["document", "presentation"]
]


class Scraper:
    def __init__(self, supported_mimetypes=None):
        self._scopes = SCOPES
        self._supported_mimetypes = (
            SUPPORTED_MIMETYPES if supported_mimetypes is None else supported_mimetypes
        )
        self._credentials = self._get_auth()
        self._service = discovery.build(
            "drive", "v3", http=self._credentials.authorize(Http())
        )
        self._files_resource = self._service.files()
        self._permissions_resource = self._service.permissions()

    def _get_auth(self):
        store = file.Storage("storage.json")
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets("client_id.json", SCOPES)
            creds = tools.run_flow(flow, store)
        return creds

    def list_drive_files(self) -> List[Document]:
        all_files = self._files_resource.list().execute()["files"]
        supported_files = [
            f for f in all_files if f["mimeType"] in self._supported_mimetypes
        ]
        documents = [
            Document.deserialize(
                {
                    "id": f["id"],
                    "title": f["name"],
                    "content": self._get_file_text_content(f["id"]),
                }
            )
            for f in supported_files
        ]
        return documents

    def _get_file_text_content(self, document_id: str) -> str:
        content = self._files_resource.export_media(
            fileId=document_id, mimeType="text/plain"
        ).execute()
        return self._clean_file_content(content)

    def _clean_file_content(self, text: bytes) -> str:
        text = strip_whitespace(replace_unicode_quotations(decode_string(text)))
        return text

    def list_users_from_documents(self, files: List[Document]) -> List[User]:
        user_emails_with_permissions = defaultdict(list)
        for f in files:
            permissions = self.get_file_permissions(f)
            for email, permission in permissions:
                user_emails_with_permissions[email].append(permission)

        users = []
        for email, permissions in user_emails_with_permissions.items():
            users.append(
                User.deserialize(
                    {
                        "email": email,
                        "permissions": [p.serialize() for p in permissions],
                    }
                )
            )
        return users

    def get_file_permissions(self, file: Document) -> List[Tuple[str, Permission]]:
        # Make sure we're not saving the document content
        file_permissions = self._permissions_resource.list(
            fileId=file.id, fields="*"
        ).execute()["permissions"]

        return [
            (
                permission["emailAddress"],
                Permission.deserialize(
                    {
                        "id": permission["id"],
                        "role": permission["role"],
                        "document_id": file.id,
                    }
                ),
            )
            for permission in file_permissions
        ]
