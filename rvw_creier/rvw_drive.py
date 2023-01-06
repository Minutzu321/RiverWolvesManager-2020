import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import rvw_fisiere
import os
import pickle
import io
from PIL import Image

from .rvw_image import *
from .rvw_facerecog import *

def startDriveScan():
    SCOPURI = ['https://www.googleapis.com/auth/drive']
    creds = None
    credsPath = rvw_fisiere.getCreierPath("drive","creds")
    if os.path.exists(credsPath):
        with open(credsPath+'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credsPath+'client_id.json', SCOPURI)
            creds = flow.run_local_server(port=0)
        with open(credsPath+'token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    proceseaza(service)

def proceseaza(service, tok=None):
  if tok is None:
    results = service.files().list(q="mimeType='image/jpeg' or mimeType='image/heic'",
         pageSize=1000,fields="nextPageToken, files(id, name)").execute()
  else:
    results = service.files().list(q="mimeType='image/jpeg' or mimeType='image/heic'",
         pageSize=1000,fields="nextPageToken, files(id, name)", pageToken=tok).execute()
  items = results.get('files', [])

  if not items:
      print('No files found.')
  else:
    print('Files:')
    print(len(items))
    for item in items:
      itid = item['id']
      if not photoInSystem(itid):
        request = service.files().get_media(fileId=itid)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        img = Image.open(fh)
        data = get_exif_data(img)
        timestamp = get_date_time(data)
        lat = get_lat(data)
        lng = get_lon(data)
        checkFaces(itid,img,timestamp,lat,lng)
      else:
          # print("Deja este pus "+itid)
          pass
      # print(recunoastere_faciala(img, False))
    nxt = results.get('nextPageToken', None)
    if nxt is not None:
      proceseaza(service, nxt)
  
  if tok is None:
      print("Drive scanat cu succes") 
      clearCache()

