#!/usr/bin/env python3

import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def authenticate(creds_file):
    # If modifying these scopes, delete the file token.json.
    scopes = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_file = "token.json"
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)
    else:
        creds = None
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, "w") as token:
            token.write(creds.to_json())
    return creds


def get_files(service):
    about = service.about().get(fields="user").execute()
    email = about["user"]["emailAddress"]
    files = []
    page_token = None
    while True:
        results = (
            service.files()
            .list(
                q=f"'{email}' in owners and mimeType!='application/vnd.google-apps.folder'",
                spaces="drive",
                fields="nextPageToken, files(id, name, parents)",
                pageToken=page_token,
            )
            .execute()
        )
        files.extend(results.get("files", []))
        if not files:
            raise RuntimeError("no files found.")
        page_token = results.get("nextPageToken", None)
        if page_token is None:
            break
    return files


folder_cache = {}


def get_folder_path(folder_id):
    path_parts = []
    current_id = folder_id
    while current_id:
        if current_id in folder_cache:
            folder_name, parent_id = folder_cache[current_id]
        else:
            try:
                folder = (
                    service.files()
                    .get(fileId=current_id, fields="name, parents")
                    .execute()
                )
                folder_name = folder.get("name")
                parent_id = folder.get("parents", [None])[0]
                folder_cache[current_id] = (folder_name, parent_id)
            except Exception:
                break
        path_parts.insert(0, folder_name)  # add to the front
        current_id = parent_id
    return os.path.sep.join(path_parts[1:])


def map_files(files):
    files_map = {}
    for f in files:
        file_name = f["name"]
        file_id = f["id"]
        parents = f["parents"]
        folder_path = get_folder_path(parents[0])
        file_path = (
            os.path.sep.join((folder_path, file_name)) if folder_path else file_name
        )
        files_map[file_id] = file_path
    return files_map


if __name__ == "__main__":
    creds_file = "credentials.json"
    if os.path.exists(creds_file):
        creds = authenticate(creds_file)
    else:
        sys.exit(f"can't find required '{creds_file}' file")

    service = build("drive", "v3", credentials=creds)

    try:
        files = get_files(service)
    except HttpError as e:
        sys.exit(f"an error occurred: {e}")
    except RuntimeError as e:
        sys.exit(f"error: {e}")

    files_map = map_files(files)
    for file_id, file_path in files_map.items():
        print(f"{file_id} - {file_path}")
# https://developers.google.com/workspace/drive/api/guides/manage-downloads
