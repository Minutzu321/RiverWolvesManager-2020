import requests
import json
def sendNotif(titlu,text):
  serverToken = '--'
  headers = {
          'Content-Type': 'application/json',
          'Authorization': 'key=' + serverToken,
        }
  body = {
            'data': {
                      'title': ''+titlu+'',
                      'text': ''+text+''
                    },
            "priority": "high",
            "condition": "'admin' in topics"
          }
  response = requests.post("https://fcm.googleapis.com/fcm/send", headers = headers, data=json.dumps(body))
  print(response.status_code)
  print(response.text)