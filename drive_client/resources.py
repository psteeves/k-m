from googleapiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

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

    def list_drive_files(self):
        all_files = self._files_resource.list().execute()["files"]
        return [f for f in all_files if f["mimeType"] in self._supported_mimetypes]

    def get_file_text_content(self, file_id):
        return self._files_resource.export_media(
            fileId=file_id, mimeType="text/plain"
        ).execute()

    def get_file_permissions(self, file_id):
        return self._permissions_resource.list(fileId=file_id, fields="*").execute()[
            "permissions"
        ]

    def get_permission_details(self, file_id, permission_id):
        return self._permissions_resource.get(
            fileId=file_id, permissionId=permission_id, fields="*"
        ).execute()
