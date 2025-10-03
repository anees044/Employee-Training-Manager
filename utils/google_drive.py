import os
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload,MediaIoBaseDownload
from googleapiclient.errors import HttpError
from django.http import Http404


SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def get_drive_service():
    creds = None
    token_path = "token.json"

    
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

   
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)

        
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    service = build("drive", "v3", credentials=creds)
    return service


def upload_file_to_gdrive(file_obj, filename, folder_id=None):
    service = get_drive_service()

    file_metadata = {"name": filename}
    if folder_id:
        file_metadata["parents"] = [folder_id]

    media = MediaIoBaseUpload(file_obj, mimetype=file_obj.content_type)

    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, name, parents"
    ).execute()

    return uploaded_file


def download_file_from_drive(file_id):
    """
    Download a file from Google Drive using its file_id.
    Returns (filename, mime_type, file_bytes).
    Raises Http404 if not accessible.
    """
    service = get_drive_service()

    try:
        
        meta = service.files().get(fileId=file_id, fields="name, mimeType").execute()
        file_name = meta.get("name", "download")
        mime_type = meta.get("mimeType", "application/octet-stream")

        
        req = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, req)
        done = False
        while not done:
            _, done = downloader.next_chunk()

        fh.seek(0)
        return file_name, mime_type, fh.read()

    except HttpError as e:
        raise Http404(f"Google Drive error: {e}")
    except Exception as e:
        raise Http404("Unexpected error during download")