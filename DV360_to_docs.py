from datetime import datetime
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import client
import pprint
from pandas import read_csv
from io import StringIO
import httplib2
import pygsheets
import gspread


# DoubleClickBidmanager API authetnication
credentials = ServiceAccountCredentials.from_json_keyfile_name('./secrets.json', scopes=[
    'https://www.googleapis.com/auth/doubleclickbidmanager']) # change json file name if different
service = build('doubleclickbidmanager', 'v1', credentials=credentials)


# Google Shhets API authentication (dont forget to get those from the google doubleclick API)
client_id = "your client id"
client_secret = "your client secret"
refresh_token = "your refresh token"
endpoint = "https://accounts.google.com/o/oauth2/token"
user_agent = "your user agent name"

# Call the Sheets API

spreadsheet_credentials = client.OAuth2Credentials(None, client_id, client_secret, refresh_token,
                                                   datetime(1983, 7, 14, 12), endpoint, user_agent)
service_spreadsheet = build("sheets", "v4", http=spreadsheet_credentials.authorize(httplib2.Http()))

#Requests in JSON (body is in the form of a JSON file and also the report comes back originally as JSON file
SAMPLE_SPREADSHEET_ID = 'sample spreadsheet name'
SAMPLE_RANGE_NAME = 'Sheet1!A1:AS'
filterIds = [3669131,3669132,3669133,3669134,3669135,4096732,3669136,3669137,3669138,3669139,3669140,3669141]
for filter in filterIds :

    index = str(filter)

    body = {
     "fileTypes": ["CAMPAIGN", "AD","INSERTION_ORDER","LINE_ITEM"],
     "filterType": "ADVERTISER_ID",
     "filterIds": [filter],   #3669131,3669132,3669133,3669134,3669135,4096732,3669136,3669137,3669138,3669139,3669140,3669141
     "version": "5"
     }



response = service.sdf().download(body=body).execute()


#parsing the request and creating tab delimited files due to
for key in response.keys():
    if index == "3669131":                              #here the advertiser id has to be the first one in the filterIds array
       values = read_csv(StringIO(response[key])).to_csv(f'{key}.csv', sep=',', quotechar='"', index=False)
       result = service_spreadsheet.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                            valueInputOption='RAW',
                                                            range=SAMPLE_RANGE_NAME, body=body).execute()
    else:
        values = read_csv(StringIO(response[key])).to_csv(f'{key}.csv', mode='a',  sep=',', quotechar='"', index=False, header = False)
        result = service_spreadsheet.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                            valueInputOption='RAW',
                                                            range=SAMPLE_RANGE_NAME, body=body).execute()
    







