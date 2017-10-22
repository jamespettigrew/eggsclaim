import requests

def send_sms(to, message_content):
    payload = { 
        "to" : to,
        "body" : message_content,
        "from" : "",
        "validity" : 0,
        "scheduleDelivery" : 0,
        "notifyURL" : "",
        "replyRequest" : True
    }

    auth = ('', '')
    response = requests.post('https://tapi.telstra.com/v2/messages/sms', json=payload, auth=auth)

    print(response.status_code) # TODO: REMOVE ME