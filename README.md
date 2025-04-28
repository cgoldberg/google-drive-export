# google-drive-export

### Export and archive your Google Drive data

- Copyright (c) 2025 [Corey Goldberg][github-home]
- License: [MIT][mit-license]
- Development: [GitHub][github-repo]

[github-home]: https://github.com/cgoldberg
[mit-license]: https://raw.githubusercontent.com/cgoldberg/google-drive-export/refs/heads/master/LICENSE
[github-repo]: https://github.com/cgoldberg/google-drive-export

----

### About:

This program retrieves files using the Google Drive API v3.

For more information:
- [API Overview][api-overview]
- [REST API Reference][api-reference]
- [API Guides][api-guides]

[api-overview]: https://developers.google.com/workspace/drive/api
[api-reference]: https://developers.google.com/workspace/drive/api/reference/rest/v3
[api-guides]: https://developers.google.com/workspace/drive/api/guides/about-files

----

### Requirements:

- Python 3.9+
- Packages:
  - google-api-python-client
  - google-auth-httplib2
  - google-auth-oauthlib

----

### Usage Instructions:

#### 1. Clone the repository

```
git clone https://github.com/cgoldberg/google-drive-export.git
cd google-drive-export
```

#### 2. Create a virtual environment

- On Linux/Mac:

```
python3 -m venv venv
source venv/bin/activate
```

- On Windows:

```
py -m venv venv
venv\Scripts\activate
```

#### 3. Install dependencies:

```
pip install -r requirements.txt
```

#### 4. Enable the Google Drive API

- Go to the Google Cloud console (Enable access to API)
  - https://console.cloud.google.com/flows/enableapi?apiid=drive.googleapis.com
- Create a Project
- Enable the API

#### 5. Configure the OAuth Consent screen

- Go to the Google Cloud console (Branding)
  - https://console.cloud.google.com/auth/branding
- Configure your Project
- Go to the Google Cloud console (Audience)
  - https://console.cloud.google.com/auth/audience
- Add yourself as a Test user

#### 6. Authorize credentials for a desktop application

- Go to the Google Cloud console (Clients)
  - https://console.cloud.google.com/auth/clients
  - Create a Client (Application type > Desktop app)
  - Downloaded JSON file, rename it to credentials.json, and move it to your working directory

#### 7. Run the program

```
python ./google_drive_export.py
```

- The first time you run it, a browser window will open and you will be prompted to authorize access to your Google account:
  - If you are not already signed in to your Google Account, sign in when prompted
  - If you are signed in to multiple accounts, select the account to use for authorization
  - Click Accept
- Authorization information is stored in the file system (`token.json`), so the next time you run it, you aren't prompted for authorization
