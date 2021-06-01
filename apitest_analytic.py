from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run_flow
from oauth2client.file import Storage
import httplib2

SERVICE_NAME = "youtubereporting"
VERSION = 'v1'
SCOPE = 'https://www.googleapis.com/auth/yt-analytics.readonly'
CLIENT_SECRETS_FILE = "client_secret_646770396162-8lpivh3piff4a39s9unaupr57v9c5lc0.apps.googleusercontent.com.json"  # Presuming you made this and in dir w/ it
flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=SCOPE, message=' f off ')

# 
credentials_file = 'name-of-OAuth2-file.json' # e.g., projectName-oauth2.json
storage = Storage(credentials_file) 
credentials = storage.get()   # Returns None if the file doesn't exist
if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage)  # This creates the credentials_file
reporting_api = build(SERVICE_NAME,  VERSION,  http=credentials.authorize(httplib2.Http()))
result=reporting_api.reportTypes().list().execute()

print(result)