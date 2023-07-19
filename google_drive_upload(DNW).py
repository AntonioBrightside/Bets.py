from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account


def upload_basic():
    """Insert new file.
    Returns : Id's of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - Look at https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # creds, _ = google.auth.default()
    credentials = service_account.Credentials.from_service_account_file('bets-project-10112022-4f96ba07bdbd.json')

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=credentials)

        file_metadata = {'name': r'.\data\2022-2023_data.csv',
                         'parent': '1wHmF0ES5s-Mormdr7CipbxbX6CHla_12',
                         'role': 'writer',
                         'type': 'anyone',
                         'value': 'anyone',
                         'emailAddress': 'antonio-brightside@bets-project-10112022.iam.gserviceaccount.com',
                         'supportsAllDrives': True}

        media = MediaFileUpload(r'.\data\2022-2023_data.csv',
                                mimetype='text/csv')
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id', supportsTeamDrives=True).execute()
        print(F'File ID: {file.get("id")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')


if __name__ == '__main__':
    upload_basic()
