# FAST SMS ***************************************

import requests
import json

# mention url
url = "https://www.fast2sms.com/dev/bulk"
headers = {
    'authorization': '7n9roGBusIYlFfWSj63txm10Pa4OM5dhZLkRyH2pCiwcNgAKTX9Mv2DP8Z6aTINBLuWeCGOR7gxtcsjl',
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache"
}

data = {
    'sender_id': 'CHKSMS',
    'message': 'Hey',
    'language': 'english',
    'route': 'p',
    'numbers': '8369398163'
}


def send_sms(name, number, shorten_url):
    data['numbers'] = number
    data['message'] = "Hey " + name + ", \nTrack your position in waiting through the below URL.\n"+shorten_url
    resp = requests.request("POST", url, data=data, headers=headers)
    resp_text = json.loads(resp.text)
    return resp_text


